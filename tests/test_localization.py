import os
import sys
import unittest
from unittest.mock import patch

from gui_data.localization import (
    apply_localization,
    is_simplified_chinese,
    localized_display_value,
    localized_stem_name,
    upstream_display_value,
)


class LocalizationTests(unittest.TestCase):
    def test_chinese_is_the_fork_default(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(sys, "argv", ["UVR.py"]):
            self.assertTrue(is_simplified_chinese())

    def test_english_environment_override_preserves_upstream_text(self):
        namespace = {"START_PROCESSING": "Start Processing"}
        with patch.dict(os.environ, {"UVR_LANGUAGE": "en"}), patch.object(sys, "argv", ["UVR.py"]):
            self.assertFalse(apply_localization(namespace))
        self.assertEqual(namespace["START_PROCESSING"], "Start Processing")
        self.assertEqual(namespace["UI_LANGUAGE"], "en")

    def test_command_line_override_has_priority(self):
        with patch.dict(os.environ, {"UVR_LANGUAGE": "en"}), patch.object(
            sys, "argv", ["UVR.py", "--language=zh_CN"]
        ):
            self.assertTrue(is_simplified_chinese())

    def test_internal_values_are_not_translated(self):
        namespace = {
            "START_PROCESSING": "Start Processing",
            "CHOOSE_MODEL": "Choose Model",
            "PROCESS_METHODS": ("VR Architecture", "MDX-Net", "Demucs"),
            "MAIN_FONT_NAME": "Montserrat",
            "SEC_FONT_NAME": "Century Gothic",
        }
        with patch.dict(os.environ, {"UVR_LANGUAGE": "zh_CN"}), patch.object(sys, "argv", ["UVR.py"]):
            self.assertTrue(apply_localization(namespace))

        self.assertEqual(namespace["START_PROCESSING"], "开始处理")
        self.assertEqual(namespace["CHOOSE_MODEL"], "Choose Model")
        self.assertEqual(namespace["PROCESS_METHODS"], ("VR Architecture", "MDX-Net", "Demucs"))
        self.assertEqual(namespace["MAIN_FONT_NAME"], "Microsoft YaHei UI")

    def test_stem_translation_is_display_only(self):
        with patch.dict(os.environ, {"UVR_LANGUAGE": "zh_CN"}), patch.object(sys, "argv", ["UVR.py"]):
            self.assertEqual(localized_stem_name("Vocals"), "人声")
            self.assertEqual(localized_stem_name("No Noise"), "无噪声")
            self.assertEqual(localized_stem_name("Primary Stem"), "主要音轨")
            self.assertEqual(localized_stem_name("Custom Stem"), "Custom Stem")

    def test_combobox_display_values_round_trip(self):
        with patch.dict(os.environ, {"UVR_LANGUAGE": "zh_CN"}), patch.object(sys, "argv", ["UVR.py"]):
            self.assertEqual(localized_display_value("Choose Model"), "选择模型")
            self.assertEqual(localized_display_value("MDX-Net"), "MDX-Net")
            self.assertEqual(upstream_display_value("选择模型"), "Choose Model")
            self.assertEqual(upstream_display_value("MDX-Net"), "MDX-Net")


if __name__ == "__main__":
    unittest.main()
