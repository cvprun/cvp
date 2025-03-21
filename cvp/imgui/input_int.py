# -*- coding: utf-8 -*-

from typing import NamedTuple

from imgui_bundle import imgui


class InputIntResult(NamedTuple):
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

    def __bool__(self) -> bool:
        return self.changed


def input_int(
    label: str,
    value: int,
    step=1,
    step_fast=100,
    flags=0,
):
    result = imgui.input_int(label, value, step, step_fast, flags)
    return InputIntResult.from_raw(result)
