# -*- coding: utf-8 -*-

import platform

from cvp.apps.player.modes.system._base import BaseSystem
from cvp.arguments import version
from cvp.assets.fonts.mdi import INFORMATION_VARIANT_CIRCLE
from cvp.context.context import Context
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.types.override import override


class AboutSystem(BaseSystem):
    __cvp_menu_name__ = "About"
    __cvp_menu_icon__ = INFORMATION_VARIANT_CIRCLE

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def on_process(self) -> None:
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
