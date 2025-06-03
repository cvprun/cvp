# -*- coding: utf-8 -*-

from typing import NamedTuple, Tuple, Union

from imgui_bundle import imgui

from cvp.imgui.flags.slider import SliderFlags


class SliderInt2Result(NamedTuple):
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
        value0, value1 = value
        assert isinstance(value0, int)
        assert isinstance(value1, int)
        return cls(changed, (value0, value1))

    def __bool__(self):
        return self.changed


def slider_int2(
    label: str,
    value0: int,
    value1: int,
    min_value: int,
    max_value: int,
    fmt="%d",
    flags: Union[SliderFlags, int] = 0,
):
    if isinstance(flags, SliderFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    values = [value0, value1]
    result = imgui.slider_int2(label, values, min_value, max_value, fmt, flags)
    return SliderInt2Result.from_raw(result)
