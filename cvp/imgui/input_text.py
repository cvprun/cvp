# -*- coding: utf-8 -*-

from typing import NamedTuple, Union

from imgui_bundle import imgui

from cvp.imgui.flags.input_text import InputTextFlags


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


def input_text(label: str, value: str, flags: Union[InputTextFlags, int] = 0):
    if isinstance(flags, InputTextFlags):
        flags = int(flags)
    assert isinstance(flags, int)
    result = imgui.input_text(label, value, flags)
    return InputTextResult.from_raw(result)
