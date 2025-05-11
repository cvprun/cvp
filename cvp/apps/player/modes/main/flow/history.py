# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.apps.player.modes.main.position import DockPosition
from cvp.context.context import Context
from cvp.flow.graph import FlowGraph, GraphKey
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import AUTO_RESIZE_Y
from cvp.imgui.flags.selectable import ALLOW_DOUBLE_CLICK
from cvp.imgui.text_centered import text_centered
from cvp.imgui.tooltip import hovered_tooltip_text
from cvp.types.override import override


class HistoryFlowWindow(BaseWindow):
    __cvp_window_name__ = "History"
    __cvp_window_position__ = DockPosition.right_bottom

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def focused_graph(self):
        return self.context.flows.graphs.get(GraphKey(self.focused_key))

    @override
    def do_main_process(self) -> None:
        with begin_child_context("Toolbar", child_flags=AUTO_RESIZE_Y):
            self.do_toolbar_process()
        imgui.separator()
        with begin_child_context("History"):
            if graph := self.focused_graph:
                self.do_history_process(graph)
            else:
                text_centered("Please select a graph")

    @staticmethod
    def do_toolbar_process() -> None:
        pass

    @staticmethod
    def do_history_process(graph: FlowGraph) -> None:
        for i, record in enumerate(graph.history):
            label = f"[{i}] {record.title}"
            selected = i == graph.history.cursor_index
            if imgui.selectable(label, selected, ALLOW_DOUBLE_CLICK)[0]:
                if imgui.is_mouse_double_clicked(0):
                    graph.load_history(i)
            if record.details:
                hovered_tooltip_text(record.details)
