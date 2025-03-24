# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.imgui.flags.selectable import ALLOW_DOUBLE_CLICK
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.canvas.tabs import FlowCanvasTabs
from cvp.widgets.tab import TabItem


class HistoryTab(TabItem[FlowCanvasTabs]):
    def __init__(self, context: RendererContext):
        super().__init__(context, "History")

    @override
    def on_item(self, item: FlowCanvasTabs) -> None:
        canvas = item.canvas
        if canvas is None:
            self.on_none()
            return

        flags = ALLOW_DOUBLE_CLICK
        cursor_index = canvas.history.cursor_index
        for i, record in enumerate(canvas.history):
            if imgui.selectable(f"[{i}] {record.title}", i == cursor_index, flags)[0]:
                if imgui.is_mouse_double_clicked(0):
                    with canvas:
                        canvas.load_history(i)

            if record.details and imgui.is_item_hovered():
                if imgui.begin_tooltip():
                    try:
                        imgui.text_unformatted(record.details)
                    finally:
                        imgui.end_tooltip()
