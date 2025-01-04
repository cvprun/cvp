# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.imgui.fonts.mapper import FontMapper
from cvp.types.override import override
from cvp.widgets.tab import TabItem
from cvp.windows.flow.cursor import FlowCursor


class HistoryTab(TabItem[FlowCursor]):
    def __init__(self, context: Context, fonts: FontMapper):
        super().__init__(context, "History")
        self._fonts = fonts

    @override
    def on_item(self, item: FlowCursor) -> None:
        graph = item.graph
        if graph is None:
            self.on_none()
            return

        imgui.bullet_text("History 1")
        imgui.bullet_text("History 2")
        imgui.bullet_text("History 3")
