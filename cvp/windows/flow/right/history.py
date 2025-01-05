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
        canvas = item.canvas
        if canvas is None:
            self.on_none()
            return

        flags = imgui.SELECTABLE_ALLOW_DOUBLE_CLICK
        cursor_index = canvas.history.cursor_index
        for i, record in enumerate(canvas.history):
            if imgui.selectable(f"[{i}] {record.title}", i == cursor_index, flags)[0]:
                if imgui.is_mouse_double_clicked(0):
                    with canvas:
                        canvas.load_history(i)

            if record.details and imgui.is_item_hovered():
                with imgui.begin_tooltip():
                    imgui.text_unformatted(record.details)
