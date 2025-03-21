# -*- coding: utf-8 -*-

from typing import NamedTuple

from imgui_bundle import imgui


class DragFloatResult(NamedTuple):
    clicked: bool
    value: float

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        clicked = result[0]
        value = result[1]
        assert isinstance(clicked, bool)
        assert isinstance(value, float)
        return cls(clicked, value)

    def __bool__(self):
        return self.clicked


def drag_float(
    label: str,
    value: float,
    change_speed=1.0,
    min_value=0.0,
    max_value=0.0,
    fmt="%.3f",
    flags=0,
    power=1.0,
):
    result = imgui.drag_float(
        label, value, change_speed, min_value, max_value, fmt, flags, power
    )
    return DragFloatResult.from_raw(result)
