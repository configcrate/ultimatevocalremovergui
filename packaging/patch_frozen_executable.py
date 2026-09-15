"""Rebuild UVR's PyInstaller executable with the localized entry point.

This intentionally preserves the upstream frozen runtime and its dependency
archive.  Only the top-level ``UVR`` script is replaced and
``gui_data.localization`` is added to the embedded PYZ archive.  Run this
script with the same Python minor version used by the upstream executable.

The output is a drop-in replacement for ``UVR.exe`` in the official Windows
installation directory; it is not useful on its own.
"""

from __future__ import annotations

import argparse
import importlib.util
import marshal
import os
from pathlib import Path
import struct
import zlib


COOKIE_MAGIC = b"MEI\x0c\x0b\x0a\x0b\x0e"
COOKIE_FORMAT = "!8sIIII64s"
COOKIE_SIZE = struct.calcsize(COOKIE_FORMAT)
TOC_ENTRY_FORMAT = "!IIIIBc"
TOC_ENTRY_SIZE = struct.calcsize(TOC_ENTRY_FORMAT)
PYZ_MAGIC = b"PYZ\0"
PYZ_HEADER_SIZE = 17


def _compile(path: Path, filename: str):
    source = path.read_text(encoding="utf-8")
    return compile(source, filename, "exec", dont_inherit=True, optimize=0)


def _read_carchive(executable: Path):
    payload = executable.read_bytes()
    cookie_pos = payload.rfind(COOKIE_MAGIC)
    if cookie_pos < 0 or cookie_pos + COOKIE_SIZE > len(payload):
        raise ValueError(f"No supported PyInstaller cookie found in {executable}")

    magic, archive_length, toc_offset, toc_length, pyvers, pylib_raw = struct.unpack(
        COOKIE_FORMAT, payload[cookie_pos : cookie_pos + COOKIE_SIZE]
    )
    if magic != COOKIE_MAGIC:
        raise ValueError("Invalid PyInstaller archive cookie")

    archive_start = cookie_pos + COOKIE_SIZE - archive_length
    toc_start = archive_start + toc_offset
    toc_end = toc_start + toc_length
    entries = []
    cursor = toc_start
    while cursor < toc_end:
        header = payload[cursor : cursor + TOC_ENTRY_SIZE]
        entry_length, offset, compressed_size, size, compressed, typecode = struct.unpack(
            TOC_ENTRY_FORMAT, header
        )
        name_raw = payload[cursor + TOC_ENTRY_SIZE : cursor + entry_length]
        name = name_raw.split(b"\0", 1)[0].decode("utf-8")
        raw = payload[
            archive_start + offset : archive_start + offset + compressed_size
        ]
        entries.append(
            {
                "name": name,
                "raw": raw,
                "compressed_size": compressed_size,
                "size": size,
                "compressed": compressed,
                "typecode": typecode,
            }
        )
        cursor += entry_length

    pylib_name = pylib_raw.split(b"\0", 1)[0]
    return payload[:archive_start], entries, pyvers, pylib_name


def _patch_pyz(pyz_raw: bytes, source_root: Path) -> bytes:
    if pyz_raw[:4] != PYZ_MAGIC:
        raise ValueError("Embedded PYZ archive has an invalid signature")
    if pyz_raw[4:8] != importlib.util.MAGIC_NUMBER:
        raise RuntimeError(
            "Python bytecode version mismatch: run this builder with the same "
            "Python minor version as the upstream executable"
        )

    toc_offset = struct.unpack("!i", pyz_raw[8:12])[0]
    original_toc = marshal.loads(pyz_raw[toc_offset:])
    if isinstance(original_toc, dict):
        toc_items = list(original_toc.items())
    else:
        toc_items = list(original_toc)

    replacements = {
        "__version__": source_root / "__version__.py",
        "gui_data.localization": source_root / "gui_data" / "localization.py",
    }
    existing_types = {
        name: meta[0] for name, meta in toc_items if name in replacements
    }
    toc_items = [(name, meta) for name, meta in toc_items if name not in replacements]

    output = bytearray(pyz_raw[:PYZ_HEADER_SIZE])
    rebuilt_toc = []
    for name, (typecode, offset, length) in toc_items:
        new_offset = len(output)
        output.extend(pyz_raw[offset : offset + length])
        rebuilt_toc.append((name, (typecode, new_offset, length)))

    for module_name, module_path in replacements.items():
        code = _compile(module_path, module_name.replace(".", "/") + ".py")
        blob = zlib.compress(marshal.dumps(code), level=6)
        rebuilt_toc.append(
            (module_name, (existing_types.get(module_name, 0), len(output), len(blob)))
        )
        output.extend(blob)

    new_toc_offset = len(output)
    output.extend(marshal.dumps(rebuilt_toc))
    output[8:12] = struct.pack("!i", new_toc_offset)
    return bytes(output)


def _serialize_toc(entries):
    serialized = []
    for entry in entries:
        name = entry["name"].encode("utf-8")
        name_length = len(name) + 1
        entry_length = TOC_ENTRY_SIZE + name_length
        if entry_length % 16:
            name_length += 16 - (entry_length % 16)
        serialized.append(
            struct.pack(
                TOC_ENTRY_FORMAT + f"{name_length}s",
                TOC_ENTRY_SIZE + name_length,
                entry["offset"],
                entry["compressed_size"],
                entry["size"],
                entry["compressed"],
                entry["typecode"],
                name,
            )
        )
    return b"".join(serialized)


def rebuild(upstream_exe: Path, source_root: Path, output_exe: Path) -> None:
    bootloader, entries, pyvers, pylib_name = _read_carchive(upstream_exe)
    running_pyvers = 100 * os.sys.version_info.major + os.sys.version_info.minor
    if running_pyvers != pyvers:
        raise RuntimeError(
            f"Upstream uses Python {pyvers // 100}.{pyvers % 100}, but this "
            f"builder is running Python {os.sys.version_info.major}."
            f"{os.sys.version_info.minor}"
        )

    rebuilt_entries = []
    archive_data = bytearray()
    for entry in entries:
        if entry["name"] == "UVR":
            code = _compile(source_root / "UVR.py", "UVR.py")
            uncompressed = marshal.dumps(code)
            raw = zlib.compress(uncompressed, level=9)
            entry = {
                **entry,
                "raw": raw,
                "compressed_size": len(raw),
                "size": len(uncompressed),
                "compressed": 1,
            }
        elif entry["name"] == "PYZ-00.pyz":
            raw = _patch_pyz(entry["raw"], source_root)
            entry = {
                **entry,
                "raw": raw,
                "compressed_size": len(raw),
                "size": len(raw),
                "compressed": 0,
            }

        entry = {**entry, "offset": len(archive_data)}
        archive_data.extend(entry["raw"])
        rebuilt_entries.append(entry)

    toc = _serialize_toc(rebuilt_entries)
    archive_length = len(archive_data) + len(toc) + COOKIE_SIZE
    cookie = struct.pack(
        COOKIE_FORMAT,
        COOKIE_MAGIC,
        archive_length,
        len(archive_data),
        len(toc),
        pyvers,
        pylib_name,
    )

    output_exe.parent.mkdir(parents=True, exist_ok=True)
    output_exe.write_bytes(bootloader + archive_data + toc + cookie)
    print(f"Created {output_exe} ({output_exe.stat().st_size:,} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("upstream_exe", type=Path)
    parser.add_argument("source_root", type=Path)
    parser.add_argument("output_exe", type=Path)
    args = parser.parse_args()
    rebuild(
        args.upstream_exe.resolve(),
        args.source_root.resolve(),
        args.output_exe.resolve(),
    )


if __name__ == "__main__":
    main()
