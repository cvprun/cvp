# -*- coding: utf-8 -*-

from datetime import date

from imgui_bundle import imgui

from cvp.imgui.drag_date import drag_date
from cvp.renderer.pygame.demos.simple import run_simple_demo


class OnFrame:
    def __init__(self):
        self._date = date.today()
        self._small_input_width = False

    def __call__(self):
        if imgui.button("Today"):
            self._date = date.today()

        self._small_input_width = imgui.checkbox(
            "Min Input Width",
            self._small_input_width,
        )[1]

        if result := drag_date(
            "InputDateDemo",
            self._date,
            small_input_width=self._small_input_width,
        ):
            self._date = result.value

        imgui.input_text_with_hint("Ruler", "imgui.calc_item_width()", str())


if __name__ == "__main__":
    run_simple_demo(OnFrame(), force_egl=True, use_accelerate=False)
