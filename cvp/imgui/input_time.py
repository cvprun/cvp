# -*- coding: utf-8 -*-

from datetime import time
from typing import NamedTuple, Union

from imgui_bundle import imgui

from cvp.imgui.drag_int import drag_int
from cvp.imgui.flags.input_text import InputTextFlags


class InputTimeResult(NamedTuple):
    changed: bool
    value: time

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        value = result[1]
        assert isinstance(changed, bool)
        assert isinstance(value, time)
        return cls(changed, value)

    def __bool__(self):
        return self.changed


def input_time(
    label: str,
    value: time,
    flags: Union[InputTextFlags, int] = 0,
):
    if isinstance(flags, InputTextFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    imgui.push_id(label)
    try:
        hour = drag_int(
            label=f"##Time.Hour",
            value=value.hour,
            min_value=0,
            max_value=23,
            flags=flags,
        )

        imgui.same_line()
        imgui.text(":")
        imgui.same_line()

        minute = drag_int(
            label=f"##Time.Minute",
            value=value.minute,
            min_value=0,
            max_value=59,
            flags=flags,
        )

        imgui.same_line()
        imgui.text(":")
        imgui.same_line()

        second = drag_int(
            label=f"##Time.Second",
            value=value.second,
            min_value=0,
            max_value=59,
            flags=flags,
        )

        imgui.same_line()
        imgui.text(".")
        imgui.same_line()

        microsecond = drag_int(
            label=f"##Time.Microsecond",
            value=value.microsecond,
            min_value=0,
            max_value=999_999,
            flags=flags,
        )
    finally:
        imgui.pop_id()

    changed = any((hour[0], minute[0], second[0], microsecond[0]))
    if changed:
        value = time(
            hour=hour[1],
            minute=minute[1],
            second=second[1],
            microsecond=microsecond[1],
            tzinfo=None,
        )

    return InputTimeResult.from_raw((changed, value))
