# -*- coding: utf-8 -*-

from typing import Optional

from imgui_bundle import imgui

from cvp.apps.player.modes.flow._base import BaseFlowWindow
from cvp.apps.player.windows.graph import FlowGraphWindow
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.drag_types import DRAG_FLOW_GRAPH
from cvp.imgui.push_item_width import align_right_side
from cvp.types.override import override


class GraphsFlowWindow(BaseFlowWindow):
    __cvp_flow_window_name__ = "Graphs"

    def __init__(self, context: Context):
        super().__init__(context)
        self._filter = str()

    @override
    def do_process(self, graph: Optional[FlowGraphWindow]) -> None:
        with begin_context(self.get_window_name()):
            self.do_child_process()

    def do_child_process(self) -> None:
        with align_right_side():
            filter_result = imgui.input_text_with_hint(
                "###Filter",
                "Filter...",
                self._filter,
            )
            self._filter = filter_result[1]

        for graph in self._context.flows.graphs.values():
            if self._filter and graph.name.find(self._filter) == -1:
                continue

            imgui.selectable(f"{graph.name}###{graph.key}", p_selected=False)
            if imgui.begin_drag_drop_source():
                try:
                    data = graph.key.encode()
                    imgui.set_drag_drop_payload(DRAG_FLOW_GRAPH, data, len(data))
                    imgui.text(graph.name)
                finally:
                    imgui.end_drag_drop_source()
