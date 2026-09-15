from pathlib import Path
import unittest


class SourceSafetyTests(unittest.TestCase):
    def test_startup_cleanup_does_not_delete_text_files(self):
        source = Path("UVR.py").read_text(encoding="utf-8")
        self.assertNotIn("'.aes', '.txt', '.tmp'", source)
        self.assertIn("EXTENSIONS = ('.aes', '.tmp')", source)


if __name__ == "__main__":
    unittest.main()

