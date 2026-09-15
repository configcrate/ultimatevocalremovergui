# Ultimate Vocal Remover GUI 简体中文版

> 非官方简体中文本地化版本，由 [ConfigCrate](https://configcrate.com/) 维护。
>
> 软件、音频分离算法和核心模型均来自 UVR 原作者团队。我们只负责中文界面、中文教程与兼容性维护。

[查看 Anjok07 制作的英文原版](https://github.com/Anjok07/ultimatevocalremovergui)

![Ultimate Vocal Remover 简体中文主界面](docs/screenshots/main-zh-cn.png)

## 这个软件有什么用？

Ultimate Vocal Remover GUI 是一款免费的 AI 音频分离工具，可以从歌曲中分离：

- 人声与伴奏
- 鼓、贝斯、钢琴、吉他等独立音轨
- 和声、混响、噪声等特定声音

全部处理都在本地电脑完成，不需要上传音频。

## 中文版改了什么？

- 主界面按钮、标题和常用提示改为简体中文
- 模型选择和已保存设置等占位文字改为中文
- 常见错误、完成状态和下载提示改为中文
- 使用 Windows 自带的微软雅黑 UI，避免中文显示成方框
- 保持模型名称和内部设置值不变，可以继续使用原版模型与配置
- 修复源码启动时误删 `requirements.txt` 和 Demucs 模型清单的问题
- 修复新版 Python 环境下两个已经失效的安装依赖

部分高级参数仍保留原名称，方便查找模型资料，也能避免翻译改变程序内部逻辑。

## 最简单的使用方法

1. 点击“选择音频”，选中要处理的歌曲。
2. 点击“选择输出位置”，指定结果保存文件夹。
3. 在“选择处理方式”中选择 `MDX-Net`、`VR 人声分离` 或 `Demucs`。
4. 选择对应模型。没有模型时，可以在设置中的“模型下载中心”下载。
5. 选择想要分离的音轨，例如人声或伴奏。
6. 点击“开始处理”，等待任务完成。

如果只是想快速去除歌曲人声，建议先使用 MDX-Net 的常用人声模型。不同歌曲适合的模型可能不同，可以使用同一首歌测试几个模型并比较结果。

## 下载与安装

Windows 10/11 64 位用户可以直接下载完整安装包：

**[下载 Ultimate Vocal Remover 简体中文版](https://github.com/configcrate/ultimatevocalremovergui/releases/latest/download/UVR_v5.6.0_zh-CN_setup.exe)**

下载后双击安装即可，不需要另装 Python、FFmpeg 或 AI 运算库。安装包约 1.5 GB，安装后约占 5.2 GB，包含 NVIDIA/CUDA 运行库和两个入门模型。

安装程序目前没有商业代码签名证书，因此 Windows 可能显示“未知发布者”或 SmartScreen 提示。请只从本仓库的 Releases 页面下载，并在发布页核对 SHA-256 校验值。

需要二次开发时，也可以从源码运行：

从源码运行：

```powershell
python -m pip install -r requirements.txt
python UVR.py
```

源码依赖体积同样较大，因为程序需要 PyTorch、ONNX Runtime 和音频处理组件。

## 临时切换回英文界面

中文版默认显示简体中文。如需临时切换为英文，可以执行：

```powershell
python UVR.py --language=en
```

日常使用英文版时，建议直接下载和使用[原作者维护的英文原版](https://github.com/Anjok07/ultimatevocalremovergui)。

## 常见问题

### 没有可选模型

打开设置，在“模型下载中心”选择并下载模型。模型文件通常较大，下载时间取决于网络状况。

### 处理 MP3 时提示 FFmpeg 错误

完整 Windows 安装包已经包含 FFmpeg。从源码运行时，请安装 FFmpeg，或者把 `ffmpeg.exe` 放入程序目录。

### 显存或内存不足

尝试降低 Segment（分段大小）或 Window Size（窗口大小），关闭其他占用显存的程序，或者改用 CPU 处理。

### 中文显示成方框

Windows 中文版默认使用系统自带的“微软雅黑 UI”。其他系统可以在 UVR 字体设置中选择支持中文的字体。

## 原作者与项目来源

- 原项目：[Anjok07/ultimatevocalremovergui](https://github.com/Anjok07/ultimatevocalremovergui)
- 核心开发者：[Anjok07](https://github.com/Anjok07)、[aufr33](https://github.com/aufr33)
- 中文本地化维护：[ConfigCrate](https://configcrate.com/)

本仓库保留上游完整 Git 历史、作者信息和项目署名。UVR 上游声明代码采用 MIT License；仓库还包含带有各自许可证声明的第三方组件，使用和分发时请继续遵守对应条款。

本项目是非官方中文本地化版本，与 UVR 原作者没有官方隶属关系。详细来源说明请查看 [NOTICE.md](NOTICE.md)。
