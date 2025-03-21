# -*- coding: utf-8 -*-

from typing import NamedTuple, Tuple

from imgui_bundle import imgui


class DragFloat2Result(NamedTuple):
    clicked: bool
    values: Tuple[float, float]

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        clicked = result[0]
        values = result[1]
        assert isinstance(clicked, bool)
        assert isinstance(values, tuple)
        assert len(values) == 2
        v0 = values[0]
        v1 = values[1]
        assert isinstance(v0, float)
        assert isinstance(v1, float)
        return cls(clicked, (v0, v1))

    def __bool__(self):
        return self.clicked

    @property
    def value0(self):
        return self.values[0]

    @property
    def value1(self):
        return self.values[1]


def drag_float2(
    label: str,
    value0: float,
    value1: float,
    change_speed=1.0,
    min_value=0.0,
    max_value=0.0,
    fmt="%.3f",
    flags=0,
    power=1.0,
):
    result = imgui.drag_float2(
        label, value0, value1, change_speed, min_value, max_value, fmt, flags, power
    )
    return DragFloat2Result.from_raw(result)
