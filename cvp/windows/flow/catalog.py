# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.imgui.drag_types import DRAG_FLOW_NODE_TYPE
from cvp.renderer.widget.interface import WidgetInterface
from cvp.types.override import override


class Catalog(WidgetInterface):
    def __init__(self, context: Context):
        self._context = context
        self._catalog = self._context.fm.nodes

    @override
    def on_process(self) -> None:
        imgui.text("Catalogs:")
        for node in self._context.fm.nodes.values():
            imgui.selectable(node.path)
            with imgui.begin_drag_drop_source() as drag_drop_src:
                if drag_drop_src.dragging:
                    payload = node.path.encode()
                    imgui.set_drag_drop_payload(DRAG_FLOW_NODE_TYPE, payload)
                    imgui.text(node.path)
