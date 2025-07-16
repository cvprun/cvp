# -*- coding: utf-8 -*-

from datetime import datetime

from imgui_bundle import imgui

from cvp.imgui.combo_timezone import combo_timezone
from cvp.renderer.pygame.demos.simple import run_simple_demo


class OnFrame:
    def __init__(self):
        self._current = 0
        self._datetime = datetime.now().astimezone()
        self._filter = str()

    def __call__(self):
        if imgui.button("Now"):
            self._datetime = datetime.now().astimezone()

        tzname = self._datetime.tzname()
        imgui.text(f"TZNAME: {tzname}")

        offset = self._datetime.utcoffset()
        imgui.text(f"OFFSET: {offset}")

        if result := combo_timezone(
            "Timezone",
            self._current,
            20,
            filter_value=self._filter,
        ):
            self._current = result.value
            self._filter = result.filter_value


if __name__ == "__main__":
    run_simple_demo(OnFrame(), force_egl=True, use_accelerate=False)
