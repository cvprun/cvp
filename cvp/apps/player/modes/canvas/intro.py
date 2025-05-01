# -*- coding: utf-8 -*-

from typing import Optional

from imgui_bundle import imgui

from cvp.apps.player.modes.canvas._base import BaseCanvasWindow
from cvp.apps.player.windows.canvas import CanvasWindow
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import AUTO_RESIZE_Y
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override


class IntroCanvasWindow(BaseCanvasWindow):
    __cvp_canvas_window_name__ = "Intro"

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def do_process(self, window: Optional[CanvasWindow]) -> None:
        with begin_context(self.get_window_name()):
            with begin_child_context("Toolbar", child_flags=AUTO_RESIZE_Y):
                self.do_toolbar_process()
            imgui.separator()
            with begin_child_context("Main"):
                if window is not None:
                    self.do_child_process()
                else:
                    text_centered("Please select a canvas")

    def do_toolbar_process(self) -> None:
        pass

    def do_child_process(self) -> None:
        pass
