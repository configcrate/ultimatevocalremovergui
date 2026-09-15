"""Small, display-only localization layer for the ConfigCrate fork.

The upstream application uses many English strings as internal values.  This
module deliberately translates only labels, buttons, help text and messages so
that saved settings and processing logic remain compatible with upstream UVR.

The Simplified Chinese edition is enabled by default.  Set ``UVR_LANGUAGE=en``
or launch with ``--language=en`` to use the original English interface.
"""

from __future__ import annotations

import os
import sys
from typing import MutableMapping


ZH_CN = "zh_CN"
EN = "en"
CHINESE_FONT = "Microsoft YaHei UI"


def _requested_language() -> str:
    """Return the requested UI language without consuming command-line args."""
    for index, argument in enumerate(sys.argv[1:]):
        if argument.startswith("--language="):
            return argument.split("=", 1)[1].strip().lower()
        if argument.startswith("--lang="):
            return argument.split("=", 1)[1].strip().lower()
        if argument in ("--language", "--lang"):
            actual_index = index + 2
            if actual_index < len(sys.argv):
                return sys.argv[actual_index].strip().lower()

    return os.environ.get("UVR_LANGUAGE", ZH_CN).strip().lower()


def is_simplified_chinese() -> bool:
    return _requested_language().replace("-", "_") in {
        "zh",
        "zh_cn",
        "zh_hans",
        "cn",
        "chinese",
    }


# Only names known to be presentation strings belong here.  Do not translate
# model identifiers, PROCESS_METHODS, stem values or saved-setting sentinels.
ZH_CN_TEXT = {
    # Main window
    "START_PROCESSING": "开始处理",
    "WAIT_PROCESSING": "请稍候……",
    "STOP_PROCESSING": "正在停止处理，请稍候……",
    "SELECT_INPUT_TEXT": "选择音频",
    "SELECT_OUTPUT_TEXT": "选择输出位置",
    "CHOOSE_PROC_METHOD_MAIN_LABEL": "选择处理方式",
    "SELECT_SAVED_SETTINGS_MAIN_LABEL": "选择已保存设置",
    "CHOOSE_MDX_MODEL_MAIN_LABEL": "选择 MDX-NET 模型",
    "BATCHES_MDX_MAIN_LABEL": "批处理大小",
    "VOL_COMP_MDX_MAIN_LABEL": "音量补偿",
    "SEGMENT_MDX_MAIN_LABEL": "分段大小",
    "SELECT_VR_MODEL_MAIN_LABEL": "选择 VR 模型",
    "AGGRESSION_SETTING_MAIN_LABEL": "分离强度",
    "WINDOW_SIZE_MAIN_LABEL": "窗口大小",
    "CHOOSE_DEMUCS_MODEL_MAIN_LABEL": "选择 Demucs 模型",
    "CHOOSE_STEMS_MAIN_LABEL": "选择要分离的音轨",
    "CHOOSE_SEGMENT_MAIN_LABEL": "分段",
    "ENSEMBLE_OPTIONS_MAIN_LABEL": "组合分离选项",
    "CHOOSE_MAIN_PAIR_MAIN_LABEL": "主要音轨组合",
    "CHOOSE_ENSEMBLE_ALGORITHM_MAIN_LABEL": "组合算法",
    "AVAILABLE_MODELS_MAIN_LABEL": "可用模型",
    "CHOOSE_AUDIO_TOOLS_MAIN_LABEL": "选择音频工具",
    "CHOOSE_MANUAL_ALGORITHM_MAIN_LABEL": "选择算法",
    "CHOOSE_RATE_MAIN_LABEL": "速率",
    "CHOOSE_SEMITONES_MAIN_LABEL": "半音",
    "GPU_CONVERSION_MAIN_LABEL": "使用 GPU 加速",
    "FILE_ONE_MAIN_LABEL": "主要音频",
    "FILE_TWO_MAIN_LABEL": "次要音频",
    "FILE_ONE_MATCH_MAIN_LABEL": "目标音频",
    "FILE_TWO_MATCH_MAIN_LABEL": "参考音频",
    "TIME_WINDOW_MAIN_LABEL": "时间调整",
    "INTRO_ANALYSIS_MAIN_LABEL": "前奏分析",
    "VOLUME_ADJUSTMENT_MAIN_LABEL": "音量调整",

    # Common actions and lightweight menus
    "SELECT_INPUTS": "选择输入文件",
    "SELECTED_INPUTS": "已选择的输入文件",
    "CONFIRM_ENTRIES": "确认",
    "CLOSE_WINDOW": "关闭窗口",
    "CANCEL_TEXT": "取消",
    "CONFIRM_TEXT": "确认",
    "SELECT_MODEL_TEXT": "选择模型",
    "NONE_SELECTED": "未选择",
    "SAVE_TEXT": "保存",
    "YES_TEXT": "是",
    "NO_TEXT": "否",
    "OK_TEXT": "确定",
    "DONE_TEXT": "完成",
    "DONE_MENU_TEXT": "完成",
    "COPIED_TEXT": "已复制！",
    "COPY_ALL_TEXT_TEXT": "复制全部文字",
    "OPEN_APPLICATION_DIRECTORY_TEXT": "打开程序目录",
    "OPEN_MODEL_DIRECTORY_TEXT": "打开模型目录",
    "OPEN_MODEL_FOLDER_TEXT": "打开模型文件夹",
    "OPEN_MODELS_FOLDER_TEXT": "打开模型文件夹",
    "OPEN_INPUT_DIR_TEXT": "打开输入目录",
    "REFRESH_LIST_TEXT": "刷新列表",
    "RESTART_APPLICATION_TEXT": "重新启动程序",
    "RESET_ALL_SETTINGS_TO_DEFAULT_TEXT": "恢复全部默认设置",
    "SAVE_CURRENT_SETTINGS_TEXT": "保存当前设置",
    "DELETE_USER_SAVED_SETTING_TEXT": "删除已保存设置",
    "GENERAL_MENU_TEXT": "常规设置",
    "ADDITIONAL_SETTINGS_TEXT": "其他设置",
    "ADDITIONAL_MENUS_INFORMATION_TEXT": "更多菜单与信息",
    "DOWNLOAD_CENTER_TEXT": "模型下载中心",
    "APPLICATION_DOWNLOAD_CENTER_TEXT": "模型下载中心",
    "APPLICATION_UPDATES_TEXT": "程序更新",
    "SELECT_DOWNLOAD_TEXT": "选择下载内容",
    "TRY_MANUAL_DOWNLOAD_TEXT": "尝试手动下载",
    "MANUAL_DOWNLOADS_TEXT": "手动下载",
    "STOP_DOWNLOAD_TEXT": "停止下载",
    "CHECK_FOR_UPDATES_TEXT": "检查更新",
    "LOADING_VERSION_INFO_TEXT": "正在读取版本信息……",
    "INFO_UNAVAILABLE_TEXT": "暂无信息。",
    "NO_FILES_TEXT": "没有文件",
    "CHOOSE_INPUT_TEXT": "选择输入文件",
    "VERIFY_INPUTS_TEXT": "检查输入文件",
    "AUDIO_INPUT_TOTAL_TEXT": "音频文件总数",
    "PROCESS_STARTING_TEXT": "正在开始处理…… ",
    "SECONDS_TEXT": "秒",
    "SAMPLE_MODE_CHECKBOX": lambda value: f"试听模式（{value} 秒）",

    # Main tooltips
    "STOP_HELP": "停止当前任务。\n• 停止前会弹出确认窗口。",
    "SETTINGS_HELP": "打开设置和模型下载中心。",
    "COMMAND_TEXT_HELP": "显示当前任务状态和处理进度。",
    "SAVE_CURRENT_SETTINGS_HELP": "载入或保存程序设置。",
    "INPUT_FOLDER_ENTRY_HELP": "选择一个或多个要处理的音频文件。",
    "INPUT_FOLDER_ENTRY_HELP_2": "这里显示已选择的音频文件。",
    "INPUT_FOLDER_BUTTON_HELP": "打开输入文件所在位置。",
    "OUTPUT_FOLDER_ENTRY_HELP": "选择处理结果的保存位置。",
    "OUTPUT_FOLDER_BUTTON_HELP": "打开输出文件夹。",
    "CHOOSE_MODEL_HELP": "选择用于分离音频的模型。",
    "FORMAT_SETTING_HELP": "输出格式：",

    # Progress and result text
    "PROCESS_COMPLETE": "\n处理完成\n",
    "PROCESS_COMPLETE_2": "处理完成\n",
    "PROCESS_FAILED": "处理失败，请查看错误日志\n",
    "LOADING_MODEL": "正在加载模型……",
    "INFERENCE_STEP_1": "正在运行分离……",
    "INFERENCE_STEP_2": "分离计算完成。",
    "SAVING_ALL_STEMS": "正在保存全部音轨……",
    "ENSEMBLING_OUTPUTS": "正在合并输出结果……",
    "DONE": " 完成！\n",
    "ENSEMBLES_SAVED": "组合分离结果已保存！\n\n",
    "DOWNLOAD_FAILED": "下载失败",
    "DOWNLOAD_STOPPED": "下载已停止",
    "DOWNLOAD_COMPLETE": "下载完成",
    "DOWNLOAD_UPDATE_COMPLETE": "更新下载完成",
    "NEW_UPDATE_FOUND_TEXT": lambda version: (
        f"\n\n发现新版本：{version}"
        "\n\n请在“设置”菜单中点击更新按钮下载并安装！"
    ),

    # Common dialogs (title, message)
    "INVALID_INPUT": (
        "输入无效",
        "选择的文件不存在或无效。\n\n请确认文件仍然存在，然后重试。",
    ),
    "INVALID_EXPORT": (
        "输出位置无效",
        "选择的输出文件夹无效。\n\n请确认文件夹仍然存在。",
    ),
    "INVALID_ENSEMBLE": (
        "模型数量不足",
        "组合分离至少需要选择两个模型。",
    ),
    "INVALID_MODEL": (
        "尚未选择模型",
        "请选择一个模型后再继续。",
    ),
    "ERROR_OCCURED": (
        "发生错误",
        "\n\n是否打开错误日志查看详细信息？\n",
    ),
    "STOP_PROCESS_CONFIRM": (
        "确认停止",
        "即将停止所有正在运行的任务。\n\n确定要继续吗？",
    ),
    "EXIT_PROCESS_ERROR": (
        "任务正在运行",
        "请先停止当前任务，或等待任务完成后再退出。",
    ),
    "EXIT_DOWNLOAD_ERROR": (
        "下载正在进行",
        "请先停止下载，或等待下载完成后再退出。",
    ),
    "STORAGE_ERROR": (
        "磁盘空间不足",
        "系统盘剩余空间不足。程序至少需要 3 GB 可用空间才能正常运行。",
    ),
    "INVALID_FOLDER_ERROR_TEXT": (
        "文件夹无效",
        "选择的输出位置不是有效文件夹。",
    ),
    "CONFIRM_RESTART_TEXT": (
        "确认重新启动",
        "程序将保存当前设置、停止正在运行的任务并重新启动。\n\n确定要继续吗？",
    ),
}


ZH_CN_STEMS = {
    "Primary Stem": "主要音轨",
    "Secondary Stem": "次要音轨",
    "Vocals": "人声",
    "Instrumental": "伴奏",
    "Other": "其他",
    "Drums": "鼓",
    "Bass": "贝斯",
    "Guitar": "吉他",
    "Piano": "钢琴",
    "Noise": "噪声",
    "No Noise": "无噪声",
}


ZH_CN_DISPLAY_VALUES = {
    "Choose Model": "选择模型",
    "Choose Option": "选择选项",
    "Select Saved Setting": "选择已保存设置",
    "VR Architecture": "VR 人声分离",
    "Ensemble Mode": "组合分离",
    "Audio Tools": "音频工具",
}


def localized_display_value(value: str) -> str:
    """Return a translated combobox value without changing stored settings."""
    if not is_simplified_chinese():
        return value
    return ZH_CN_DISPLAY_VALUES.get(value, value)


def upstream_display_value(value: str) -> str:
    """Convert a translated combobox value back to the upstream value."""
    if not is_simplified_chinese():
        return value
    reverse_values = {translated: upstream for upstream, translated in ZH_CN_DISPLAY_VALUES.items()}
    return reverse_values.get(value, value)


def localized_stem_name(stem: str) -> str:
    """Translate a stem for display while preserving its internal value."""
    if not is_simplified_chinese():
        return stem
    return ZH_CN_STEMS.get(stem, stem)


def apply_localization(namespace: MutableMapping[str, object]) -> bool:
    """Apply display translations to UVR's imported constant namespace."""
    if not is_simplified_chinese():
        namespace["UI_LANGUAGE"] = EN
        return False

    for name, translated_value in ZH_CN_TEXT.items():
        if name in namespace:
            namespace[name] = translated_value

    namespace["UI_LANGUAGE"] = ZH_CN
    namespace["MAIN_FONT_NAME"] = CHINESE_FONT
    namespace["SEC_FONT_NAME"] = CHINESE_FONT
    return True
