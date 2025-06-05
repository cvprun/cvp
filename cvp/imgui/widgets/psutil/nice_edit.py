# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional

import psutil
from imgui_bundle import imgui

from cvp.assets.fonts import mdi
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.flags.child import AUTO_RESIZE_Y, BORDERS
from cvp.imgui.radio_button import radio_button
from cvp.imgui.slider_int import slider_int
from cvp.values.temp import TempValue
from cvp.variables import MAX_NICE, MIN_NICE


class NiceEditResult(NamedTuple):
    changed: bool
    value: int

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        value = result[1]
        assert isinstance(changed, bool)
        assert isinstance(value, int)
        return cls(changed, value)

    def __bool__(self):
        return self.changed


def nice_edit(
    label: str,
    nice: TempValue[int],
    width: Optional[float] = None,
    *,
    top_title: Optional[str] = None,
    right_title: Optional[str] = None,
    border=False,
    no_commit=False,
) -> NiceEditResult:
    if width is None:
        width = imgui.calc_item_width()
    assert isinstance(width, float)

    with begin_child_context(
        label=label,
        size=(width, 0),
        child_flags=AUTO_RESIZE_Y | (BORDERS if border else 0),
    ):
        if top_title:
            imgui.text(top_title)
            imgui.separator()

        if psutil.WINDOWS:
            from psutil import ABOVE_NORMAL_PRIORITY_CLASS as ABOVE_NORMAL
            from psutil import BELOW_NORMAL_PRIORITY_CLASS as BELOW_NORMAL
            from psutil import HIGH_PRIORITY_CLASS as HIGH
            from psutil import IDLE_PRIORITY_CLASS as IDLE
            from psutil import NORMAL_PRIORITY_CLASS as NORMAL
            from psutil import REALTIME_PRIORITY_CLASS as REALTIME

            if radio_button("Realtime", nice.temp == REALTIME):
                nice.temp = REALTIME
            if radio_button("High", nice.temp == HIGH):
                nice.temp = HIGH
            if radio_button("Above Normal", nice.temp == ABOVE_NORMAL):
                nice.temp = ABOVE_NORMAL
            if radio_button("Normal", nice.temp == NORMAL):
                nice.temp = NORMAL
            if radio_button("Below Normal", nice.temp == BELOW_NORMAL):
                nice.temp = BELOW_NORMAL
            if radio_button("IDLE", nice.temp == IDLE):
                nice.temp = IDLE
        else:
            min_value = max(nice.value, MIN_NICE)
            max_value = MAX_NICE

            if nice_result := slider_int("##Nice", nice.temp, min_value, max_value):
                if nice.value <= nice_result.value:
                    nice.temp = nice_result.value

            imgui.text(
                "CPU usage priority setting. "
                "Higher values yield CPU time to other processes."
            )

        if button(f"{mdi.CLOSE} Cancel", disabled=not nice.changed):
            nice.reset()

        imgui.same_line()
        if button(f"{mdi.CHECK} Commit", disabled=not nice.changed):
            if not no_commit:
                nice.commit()
            return NiceEditResult(True, nice.value)

    if right_title:
        imgui.same_line(spacing=imgui.get_style().item_inner_spacing.x)
        imgui.text(right_title)

    return NiceEditResult(False, nice.value)
