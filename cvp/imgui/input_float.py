# -*- coding: utf-8 -*-

from typing import NamedTuple

from imgui_bundle import imgui


class InputFloatResult(NamedTuple):
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


def input_float(
    label: str,
    value: float,
    step=0.0,
    step_fast=0.0,
    fmt="%.3f",
    flags=0,
):
    result = imgui.input_float(
        label,
        value,
        step,
        step_fast,
        fmt,
        flags,
    )
    return InputFloatResult.from_raw(result)
