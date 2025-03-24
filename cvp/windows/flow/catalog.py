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
        if imgui.collapsing_header("Dtypes"):
            for dtype in self._context.fm.dtypes.values():
                imgui.selectable(dtype.path, p_selected=False)
                if imgui.begin_drag_drop_source():
                    try:
                        data = dtype.path.encode()
                        imgui.set_drag_drop_payload(DRAG_FLOW_DTYPE, data, len(data))
                        imgui.text(dtype.path)
                    finally:
                        imgui.end_drag_drop_source()

        if imgui.collapsing_header("Nodes"):
            for node in self._context.fm.nodes.values():
                imgui.selectable(node.path, p_selected=False)
                if imgui.begin_drag_drop_source():
                    try:
                        data = node.path.encode()
                        imgui.set_drag_drop_payload(DRAG_FLOW_NODE, data, len(data))
                        imgui.text(node.path)
                    finally:
                        imgui.end_drag_drop_source()

        if imgui.collapsing_header("Graphs"):
            for graph in self._context.fm.graphs.values():
                imgui.selectable(f"{graph.name}##{graph.key}", p_selected=False)
                if imgui.begin_drag_drop_source():
                    try:
                        data = graph.key.encode()
                        imgui.set_drag_drop_payload(DRAG_FLOW_GRAPH, data, len(data))
                        imgui.text(graph.name)
                    finally:
                        imgui.end_drag_drop_source()
