# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.flow._base import BaseFlowWindow
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import AUTO_RESIZE_Y
from cvp.imgui.flags.selectable import ALLOW_DOUBLE_CLICK
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override
from cvp.widgets.canvas.tabs import FlowCanvasTabs


class HistoryFlowWindow(BaseFlowWindow):
    __cvp_flow_window_name__ = "History"

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def do_process(self) -> None:
        with begin_context(self.get_window_name()):
            with begin_child_context("Toolbar", child_flags=AUTO_RESIZE_Y):
                self.do_toolbar_process()
            imgui.separator()
            with begin_child_context("Logging"):
                self.do_logging_process()

    @staticmethod
    def do_toolbar_process() -> None:
        pass

    @staticmethod
    def do_logging_process() -> None:
        pass

    @staticmethod
    def on_item(item: FlowCanvasTabs) -> None:
        canvas = item.canvas
        if canvas is None:
            text_centered("Please select a graph")
            return

        flags = ALLOW_DOUBLE_CLICK
        cursor_index = canvas.history.cursor_index
        for i, record in enumerate(canvas.history):
            if imgui.selectable(f"[{i}] {record.title}", i == cursor_index, flags)[0]:
                if imgui.is_mouse_double_clicked(0):
                    with canvas:
                        canvas.load_history(i)

            if record.details and imgui.is_item_hovered():
                if imgui.begin_tooltip():
                    try:
                        imgui.text_unformatted(record.details)
                    finally:
                        imgui.end_tooltip()
