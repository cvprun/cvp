# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.imgui.drag_types import DRAG_FLOW_DTYPE, DRAG_FLOW_GRAPH, DRAG_FLOW_NODE
from cvp.renderer.context import RendererContext
from cvp.renderer.widget.interface import WidgetInterface
from cvp.types.override import override


class Catalog(WidgetInterface):
    def __init__(self, context: RendererContext):
        self._context = context

    @override
    def on_process(self) -> None:
        if imgui.collapsing_header("Dtypes")[0]:
            for dtype in self._context.fm.dtypes.values():
                imgui.selectable(dtype.path)
                with imgui.begin_drag_drop_source() as drag_drop_src:
                    if drag_drop_src.dragging:
                        payload = dtype.path.encode()
                        imgui.set_drag_drop_payload(DRAG_FLOW_DTYPE, payload)
                        imgui.text(dtype.path)

        if imgui.collapsing_header("Nodes")[0]:
            for node in self._context.fm.nodes.values():
                imgui.selectable(node.path)
                with imgui.begin_drag_drop_source() as drag_drop_src:
                    if drag_drop_src.dragging:
                        payload = node.path.encode()
                        imgui.set_drag_drop_payload(DRAG_FLOW_NODE, payload)
                        imgui.text(node.path)

        if imgui.collapsing_header("Graphs")[0]:
            for graph in self._context.fm.graphs.values():
                imgui.selectable(f"{graph.name}##{graph.key}")
                with imgui.begin_drag_drop_source() as drag_drop_src:
                    if drag_drop_src.dragging:
                        payload = graph.key.encode()
                        imgui.set_drag_drop_payload(DRAG_FLOW_GRAPH, payload)
                        imgui.text(graph.name)
