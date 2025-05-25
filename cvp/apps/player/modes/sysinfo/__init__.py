# -*- coding: utf-8 -*-

import platform

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.arguments import version
from cvp.assets.fonts.mdi import INFORMATION_VARIANT_CIRCLE
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.types.override import override


class SysinfoMode(BaseMode):
    __cvp_mode_name__ = "Sysinfo"
    __cvp_mode_icon__ = INFORMATION_VARIANT_CIRCLE

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                imgui.text("System Information")
                imgui.separator()

                self.on_cvp_process()
                self.on_platform_process()

    @staticmethod
    def on_cvp_process() -> None:
        input_text_disabled("CVP Version", version())
        input_text_disabled("Python Version", platform.python_version())

    @staticmethod
    def on_platform_process() -> None:
        input_text_disabled("System", platform.system())
        input_text_disabled("Node Name", platform.node())
        input_text_disabled("Release", platform.release())
        input_text_disabled("Version", platform.version())
        input_text_disabled("Machine", platform.machine())
        input_text_disabled("Processor", platform.processor())
