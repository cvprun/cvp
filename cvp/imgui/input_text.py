# -*- coding: utf-8 -*-

from typing import NamedTuple

from imgui_bundle import imgui


class InputTextResult(NamedTuple):
    changed: bool
    value: str

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        value = result[1]
        assert isinstance(changed, bool)
        assert isinstance(value, str)
        return cls(changed, value)

    def __bool__(self):
        return self.changed


def input_text(label: str, value: str, buffer_length=-1, flags=0):
    result = imgui.input_text(label, value, buffer_length, flags)
    return InputTextResult.from_raw(result)
