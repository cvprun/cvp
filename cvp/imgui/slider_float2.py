# -*- coding: utf-8 -*-

from typing import NamedTuple, Tuple

from imgui_bundle import imgui


class SliderFloat2Result(NamedTuple):
    changed: bool
    value: Tuple[float, float]

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        value = result[1]
        assert isinstance(changed, bool)
        assert isinstance(value, tuple)
        assert len(value) == 2
        value0, value1 = value
        assert isinstance(value0, float)
        assert isinstance(value1, float)
        return cls(changed, (value0, value1))

    def __bool__(self):
        return self.changed


def slider_float2(
    label: str,
    value0: float,
    value1: float,
    min_value: float,
    max_value: float,
    fmt="%.3f",
    flags=0,
):
    values = [value0, value1]
    result = imgui.slider_float2(label, values, min_value, max_value, fmt, flags)
    return SliderFloat2Result.from_raw(result)
