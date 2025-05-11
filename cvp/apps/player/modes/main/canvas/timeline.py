# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.apps.player.modes.main.position import DockPosition
from cvp.canvas.canvas import Canvas, CanvasKey
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import AUTO_RESIZE_Y
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override


class TimelineCanvasWindow(BaseWindow):
    __cvp_window_name__ = "Timeline"
    __cvp_window_position__ = DockPosition.center_bottom

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def focused_canvas(self):
        return self.context.canvases.get(CanvasKey(self.focused_key))

    @override
    def on_main_process(self) -> None:
        with begin_child_context("Toolbar", child_flags=AUTO_RESIZE_Y):
            self.do_toolbar_process()
        imgui.separator()
        with begin_child_context("History"):
            if canvas := self.focused_canvas:
                self.do_history_process(canvas)
            else:
                text_centered("Please select a canvas")

    @staticmethod
    def do_toolbar_process() -> None:
        pass

    @staticmethod
    def do_history_process(canvas: Canvas) -> None:
        pass
