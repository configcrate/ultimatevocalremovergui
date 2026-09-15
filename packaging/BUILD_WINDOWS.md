# Windows 安装包构建说明

仓库不会提交或修改上游的二进制运行环境。构建者需要自行下载 UVR v5.6 的官方完整安装包和最终补丁，然后执行以下步骤：

1. 使用 `innoextract` 将完整安装包解压到 `.build/upstream/full`。
2. 将官方最终补丁的内容覆盖到 `.build/upstream/full/app`。
3. 使用 Python 3.9 运行 `patch_frozen_executable.py`，以官方补丁中的 `UVR.exe` 为输入。
4. 将生成的本地化 `UVR.exe` 覆盖到完整运行目录。
5. 使用 Inno Setup 6 编译 `windows-installer.iss`。

安装向导使用 Kira 维护的 Inno Setup 简体中文翻译，许可文本见
`ChineseSimplified.LICENSE`。

`patch_frozen_executable.py` 不会重新打包第三方依赖。它保留官方 PyInstaller 运行时，只替换本项目维护的 `UVR` 入口代码、版本信息和简体中文本地化模块。

发布前必须在一台没有 Python 开发环境依赖的 Windows 10/11 机器上验证安装、启动、基础分离处理和卸载。
