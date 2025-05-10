# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.apps.player.widgets.flows.selectable_graph import selectable_graph
from cvp.context.context import Context
from cvp.imgui.flags.mouse_button import MOUSE_LEFT
from cvp.imgui.push_item_width import align_right_side_context
from cvp.types.override import override


class GraphsFlowWindow(BaseWindow):
    __cvp_window_name__ = "Graphs"

    def __init__(self, context: Context):
        super().__init__(context)
        self._filter = str()

    @override
    def do_main_process(self) -> None:
        with align_right_side_context():
            filter_result = imgui.input_text_with_hint(
                "###Filter",
                "Filter graphs ...",
                self._filter,
            )
            self._filter = filter_result[1]

        for graph in self._context.flows.graphs.values():
            if self._filter and graph.name.find(self._filter) == -1:
                continue

            if selectable_graph(graph, use_drag_source=True):
                if not graph.opened and imgui.is_mouse_double_clicked(MOUSE_LEFT):
                    graph.opened = True
