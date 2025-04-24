# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.flow._base import BaseFlowWindow
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.drag_types import DRAG_FLOW_DTYPE, DRAG_FLOW_GRAPH, DRAG_FLOW_NODE
from cvp.imgui.push_item_width import align_right_side
from cvp.types.override import override


class CatalogFlowWindow(BaseFlowWindow):
    __cvp_flow_window_name__ = "Catalog"

    def __init__(self, context: Context):
        super().__init__(context)
        self._search = str()

    @override
    def do_process(self) -> None:
        with begin_context(self.get_window_name()):
            self.do_search_process()
            imgui.separator()
            self.do_dtypes_process()
            imgui.separator()
            self.do_nodes_process()
            imgui.separator()
            self.do_graphs_process()

    def do_search_process(self) -> None:
        with align_right_side():
            search_result = imgui.input_text_with_hint(
                "###Search",
                "Search catalog items...",
                self._search,
            )
            self._search = search_result[1]

    def do_dtypes_process(self) -> None:
        if not imgui.collapsing_header("Dtypes"):
            return

        for dtype in self._context.flows.dtypes.values():
            if self._search and dtype.path.find(self._search) == -1:
                continue

            imgui.selectable(dtype.path, p_selected=False)
            if imgui.begin_drag_drop_source():
                try:
                    data = dtype.path.encode()
                    imgui.set_drag_drop_payload(DRAG_FLOW_DTYPE, data, len(data))
                    imgui.text(dtype.path)
                finally:
                    imgui.end_drag_drop_source()

    def do_nodes_process(self) -> None:
        if not imgui.collapsing_header("Nodes"):
            return

        for node in self._context.flows.nodes.values():
            if self._search and node.path.find(self._search) == -1:
                continue

            imgui.selectable(node.path, p_selected=False)
            if imgui.begin_drag_drop_source():
                try:
                    data = node.path.encode()
                    imgui.set_drag_drop_payload(DRAG_FLOW_NODE, data, len(data))
                    imgui.text(node.path)
                finally:
                    imgui.end_drag_drop_source()

    def do_graphs_process(self) -> None:
        if not imgui.collapsing_header("Graphs"):
            return

        for graph in self._context.flows.graphs.values():
            if self._search and graph.name.find(self._search) == -1:
                continue

            imgui.selectable(f"{graph.name}###{graph.key}", p_selected=False)
            if imgui.begin_drag_drop_source():
                try:
                    data = graph.key.encode()
                    imgui.set_drag_drop_payload(DRAG_FLOW_GRAPH, data, len(data))
                    imgui.text(graph.name)
                finally:
                    imgui.end_drag_drop_source()
