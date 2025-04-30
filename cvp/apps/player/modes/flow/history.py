# -*- coding: utf-8 -*-

from typing import Optional

from imgui_bundle import imgui

from cvp.apps.player.modes.flow._base import BaseFlowWindow
from cvp.apps.player.windows.graph import FlowGraphWindow
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import AUTO_RESIZE_Y
from cvp.imgui.flags.selectable import ALLOW_DOUBLE_CLICK
from cvp.imgui.text_centered import text_centered
from cvp.imgui.tooltip import hovered_tooltip_text
from cvp.types.override import override


class HistoryFlowWindow(BaseFlowWindow):
    __cvp_flow_window_name__ = "History"

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def focused_graph(self):
        return self._context.flows.focused_graph

    @override
    def do_process(self, window: Optional[FlowGraphWindow]) -> None:
        with begin_context(self.get_window_name()):
            with begin_child_context("Toolbar", child_flags=AUTO_RESIZE_Y):
                self.do_toolbar_process()
            imgui.separator()
            with begin_child_context("History"):
                if window is not None:
                    self.do_history_process(window)
                else:
                    text_centered("Please select a graph")

    @staticmethod
    def do_toolbar_process() -> None:
        pass

    @staticmethod
    def do_history_process(window: FlowGraphWindow) -> None:
        for i, record in enumerate(window.history):
            label = f"[{i}] {record.title}"
            selected = i == window.history.cursor_index
            if imgui.selectable(label, selected, ALLOW_DOUBLE_CLICK)[0]:
                if imgui.is_mouse_double_clicked(0):
                    window.load_history(i)
            if record.details:
                hovered_tooltip_text(record.details)
