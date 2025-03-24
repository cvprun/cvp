# -*- coding: utf-8 -*-

from typing import NamedTuple, Tuple, Union

from imgui_bundle import imgui

from cvp.imgui.flags.input_text import InputTextFlags


class InputInt2Result(NamedTuple):
    changed: bool
    value: Tuple[int, int]

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        value = result[1]
        assert isinstance(changed, bool)
        assert isinstance(value, (tuple, list))
        assert len(value) == 2
        value0 = value[0]
        value1 = value[1]
        assert isinstance(value0, int)
        assert isinstance(value1, int)
        return cls(changed, (value0, value1))

    def __bool__(self):
        return self.changed

    @property
    def value0(self):
        return self.value[0]

    @property
    def value1(self):
        return self.value[1]


def input_int2(
    label: str,
    value0: int,
    value1: int,
    flags: Union[InputTextFlags, int] = 0,
):
    if isinstance(flags, InputTextFlags):
        flags = int(flags)
    assert isinstance(flags, int)
    result = imgui.input_int2(label, [value0, value1], flags)
    return InputInt2Result.from_raw(result)
