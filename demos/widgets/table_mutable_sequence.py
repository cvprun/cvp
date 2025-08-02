# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.imgui.fonts.defaults import add_mixed_font
from cvp.imgui.widgets.table_mutable_sequence import table_mutable_sequence
from cvp.renderer.pygame.demos.simple import SimpleDemoBase
from cvp.types.override import override


class TableMutableSequenceDemo(SimpleDemoBase):
    def __init__(self, font_name="Default", font_size=12):
        super().__init__(force_egl=True, use_accelerate=True)
        self._items = list()
        self._font_name = font_name
        self._font_size = font_size

    @override
    def on_init(self) -> None:
        imgui.get_io().fonts.clear()
        add_mixed_font(self._font_name, self._font_size)

    @override
    def on_frame(self) -> None:
        imgui.set_next_window_size((400, 0))
        imgui.begin(type(self).__name__)
        table_mutable_sequence(
            "Items",
            self._items,
            swappable=True,
            removable=True,
            insertable_callback=lambda _: str(),
        )
        imgui.end()


if __name__ == "__main__":
    TableMutableSequenceDemo().run()
