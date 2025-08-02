# -*- coding: utf-8 -*-

from datetime import datetime

from imgui_bundle import imgui

from cvp.chrono.timezones import local_tzinfo
from cvp.imgui.combo_timezone import TZINFO_MAP, combo_timezone
from cvp.renderer.pygame.demos.simple import run_simple_demo


class OnFrame:
    def __init__(self):
        self._value = local_tzinfo().name
        self._filter = str()

    def __call__(self):
        if imgui.button("Now"):
            self._value = local_tzinfo().name

        offset = datetime.now(tz=TZINFO_MAP[self._value]).utcoffset()
        imgui.text(f"OFFSET: {offset}")

        if result := combo_timezone(
            label="Timezone",
            value=self._value,
            filter_value=self._filter,
        ):
            self._value = result.tzname
            self._filter = result.filter_value


if __name__ == "__main__":
    run_simple_demo(OnFrame())
