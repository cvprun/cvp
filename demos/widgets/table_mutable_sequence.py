# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.imgui.widgets.table_mutable_sequence import table_mutable_sequence
from cvp.renderer.pygame.demos.simple import run_simple_demo


class OnFrame:
    def __init__(self):
        self._items = list()

    def __call__(self) -> None:
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
    run_simple_demo(OnFrame())
