# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.flow._base import BaseFlowWindow
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.drag_types import DRAG_FLOW_DTYPE, DRAG_FLOW_GRAPH, DRAG_FLOW_NODE
from cvp.types.override import override


class DtypesFlowWindow(BaseFlowWindow):
    __cvp_flow_window_name__ = "Dtypes"

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def do_process(self) -> None:
        with begin_context(self.get_window_name()):
            self.do_child_process()

    def do_child_process(self) -> None:
        if imgui.collapsing_header("Dtypes"):
            for dtype in self._context.flows.dtypes.values():
                imgui.selectable(dtype.path, p_selected=False)
                if imgui.begin_drag_drop_source():
                    try:
                        data = dtype.path.encode()
                        imgui.set_drag_drop_payload(DRAG_FLOW_DTYPE, data, len(data))
                        imgui.text(dtype.path)
                    finally:
                        imgui.end_drag_drop_source()

        if imgui.collapsing_header("Nodes"):
            for node in self._context.flows.nodes.values():
                imgui.selectable(node.path, p_selected=False)
                if imgui.begin_drag_drop_source():
                    try:
                        data = node.path.encode()
                        imgui.set_drag_drop_payload(DRAG_FLOW_NODE, data, len(data))
                        imgui.text(node.path)
                    finally:
                        imgui.end_drag_drop_source()

        if imgui.collapsing_header("Graphs"):
            for graph in self._context.flows.graphs.values():
                imgui.selectable(f"{graph.name}##{graph.key}", p_selected=False)
                if imgui.begin_drag_drop_source():
                    try:
                        data = graph.key.encode()
                        imgui.set_drag_drop_payload(DRAG_FLOW_GRAPH, data, len(data))
                        imgui.text(graph.name)
                    finally:
                        imgui.end_drag_drop_source()
