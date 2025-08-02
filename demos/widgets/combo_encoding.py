# -*- coding: utf-8 -*-

from cvp.imgui.combo_encoding import combo_text_encoding
from cvp.renderer.pygame.demos.simple import run_simple_demo


class OnFrame:
    def __init__(self):
        self._index = 0
        self._filter = str()

    def __call__(self):
        if result := combo_text_encoding(
            label="Encoding",
            value=self._index,
            filter_value=self._filter,
        ):
            self._index = result.value
            self._filter = result.filter_value


if __name__ == "__main__":
    run_simple_demo(OnFrame())
