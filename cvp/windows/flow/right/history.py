# -*- coding: utf-8 -*-

import imgui

from cvp.imgui.fonts.mapper import FontMapper
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.tab import TabItem
from cvp.windows.flow.canvases import Canvases


class HistoryTab(TabItem[Canvases]):
    def __init__(self, context: RendererContext, fonts: FontMapper):
        super().__init__(context, "History")
        self._fonts = fonts

    @override
    def on_item(self, item: Canvases) -> None:
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
