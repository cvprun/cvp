# -*- coding: utf-8 -*-

import imgui

from cvp.imgui.drag_types import DRAG_FLOW_DTYPE, DRAG_FLOW_NODE
from cvp.imgui.fonts.mapper import FontMapper
from cvp.renderer.context import RendererContext
from cvp.renderer.widget.interface import WidgetInterface
from cvp.types.override import override


class Catalog(WidgetInterface):
    def __init__(self, context: RendererContext, fonts: FontMapper):
        self._context = context
        self._fonts = fonts

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
