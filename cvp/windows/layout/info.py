# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.config.sections.layout import LayoutConfig
from cvp.imgui.button import button
from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.push_item_width import item_width
from cvp.imgui.text_colored import text_colored
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.tab import TabItem


class LayoutInfoTab(TabItem[LayoutConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(context, "Info")

    def get_layout_filepath(self, layout: LayoutConfig) -> str:
        return str(self.context.home.layouts.key_filepath(layout.uuid))

    def has_layout(self, layout: LayoutConfig) -> bool:
        return self.context.home.layouts.has_layout(layout.uuid)

    def save_layout(self, layout: LayoutConfig) -> None:
        self.context.home.layouts.save_layout(layout.uuid)

    def load_layout(self, layout: LayoutConfig) -> None:
        self.context.home.layouts.load_layout(layout.uuid)

    def remove_layout(self, layout: LayoutConfig) -> None:
        self.context.home.layouts.remove_layout(layout.uuid)

    @override
    def on_item(self, item: LayoutConfig) -> None:
        imgui.text("UUID:")
        input_text_disabled("## UUID", item.uuid)

        imgui.text("Name:")
        with item_width(0):
            changed_name, value_name = imgui.input_text(
                "## Name",
                item.name,
                ENTER_RETURNS_TRUE,
            )
            assert isinstance(changed_name, bool)
            assert isinstance(value_name, str)
            if changed_name:
                item.name = value_name

        imgui.text("Path:")
        input_text_disabled("## Path", self.get_layout_filepath(item))

        has_layout = self.has_layout(item)

        if button("Save"):
            self.save_layout(item)
        imgui.same_line()
        if button("Load", disabled=not has_layout):
            self.load_layout(item)
        imgui.same_line()
        if button("Remove", disabled=not has_layout):
            self.remove_layout(item)

        if has_layout:
            status_text = "Layout file exists"
            status_color = 0.0, 1.0, 0.0, 1.0
        else:
            status_text = "The layout file does not exist"
            status_color = 1.0, 0.0, 0.0, 1.0

        text_colored(status_text, status_color)
