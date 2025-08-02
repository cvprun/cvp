# -*- coding: utf-8 -*-

from datetime import datetime

from imgui_bundle import imgui

from cvp.imgui.drag_date import drag_date
from cvp.imgui.drag_time import drag_time
from cvp.renderer.pygame.demos.simple import run_simple_demo


class OnFrame:
    def __init__(self):
        self._datetime = datetime.now()
        self._date = self._datetime.date()
        self._time = self._datetime.time()
        self._small_drag_width = False

    def __call__(self):
        if imgui.button("Now"):
            self._datetime = datetime.now()
            self._date = self._datetime.date()
            self._time = self._datetime.time()

        self._small_drag_width = imgui.checkbox(
            "Small Drag Width",
            self._small_drag_width,
        )[1]

        if date_result := drag_date(
            "Drag Date",
            self._date,
            small_field_width=self._small_drag_width,
        ):
            self._date = date_result.value

        if time_result := drag_time(
            "Drag Time",
            self._time,
            small_field_width=self._small_drag_width,
        ):
            self._time = time_result.value

        imgui.input_text_with_hint("Ruler", "imgui.calc_item_width()", str())


if __name__ == "__main__":
    run_simple_demo(OnFrame(), force_egl=True, use_accelerate=False)
