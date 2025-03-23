# -*- coding: utf-8 -*-

from typing import NamedTuple

from imgui_bundle import imgui


class SliderFloatResult(NamedTuple):
    changed: bool
    value: float

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        value = result[1]
        assert isinstance(changed, bool)
        assert isinstance(value, float)
        return cls(changed, value)

    def __bool__(self):
        return self.changed


def slider_float(
    label: str,
    value: float,
    min_value: float,
    max_value: float,
    fmt="%.3f",
    flags=0,
):
    result = imgui.slider_float(label, value, min_value, max_value, fmt, flags)
    return SliderFloatResult.from_raw(result)
