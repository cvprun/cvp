# -*- coding: utf-8 -*-

from typing import NamedTuple, Tuple

from imgui_bundle import imgui


class InputFloat2Result(NamedTuple):
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

    @property
    def value0(self):
        return self.value[0]

    @property
    def value1(self):
        return self.value[1]


def input_float2(
    label: str,
    value0: float,
    value1: float,
    fmt="%.3f",
    flags=0,
):
    result = imgui.input_float2(
        label,
        value0,
        value1,
        fmt,
        flags,
    )
    return InputFloat2Result.from_raw(result)
