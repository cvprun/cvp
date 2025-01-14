# -*- coding: utf-8 -*-

from typing import Optional

import imgui

from cvp.context.context import Context
from cvp.imgui.fonts.mapper import FontMapper
from cvp.types.override import override
from cvp.widgets.tab import TabItem
from cvp.windows.flow.canvases import Canvases


class GraphsTab(TabItem[Canvases]):
    def __init__(self, context: Context, fonts: FontMapper):
        super().__init__(context, "Graphs")
        self._fonts = fonts

    @override
    def on_none(self) -> None:
        self.listbox_graphs()

    @override
    def on_item(self, item: Canvases) -> None:
        self.listbox_graphs(item)

    def listbox_graphs(self, cursor: Optional[Canvases] = None) -> None:
        flags = imgui.SELECTABLE_ALLOW_DOUBLE_CLICK
        current_uuid = str()
        if cursor is not None and cursor.opened:
            current_graph = cursor.graph
            assert current_graph is not None
            current_uuid = current_graph.uuid

        for uuid, graph in self.context.fm.items():
            imgui.bullet()
            imgui.same_line()

            label = f"{graph.name}##{uuid}"
            selected = uuid == current_uuid

            if imgui.selectable(label, selected, flags)[0]:
                if imgui.is_mouse_double_clicked(0):
                    if cursor is not None:
                        cursor.open(graph)
