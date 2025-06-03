# -*- coding: utf-8 -*-

from typing import NamedTuple, Union

from imgui_bundle import imgui

from cvp.imgui.flags.slider import SliderFlags


class SliderIntResult(NamedTuple):
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

    def __bool__(self):
        return self.changed


def slider_int(
    label: str,
    value: int,
    min_value: int,
    max_value: int,
    fmt="%d",
    flags: Union[SliderFlags, int] = 0,
):
    if isinstance(flags, SliderFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    result = imgui.slider_int(label, value, min_value, max_value, fmt, flags)
    return SliderIntResult.from_raw(result)
