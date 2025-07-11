# -*- coding: utf-8 -*-

from typing import NamedTuple, Union

from imgui_bundle import imgui

from cvp.imgui.flags.slider import SliderFlags


class DragIntResult(NamedTuple):
    clicked: bool
    value: int

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        clicked = result[0]
        value = result[1]
        assert isinstance(clicked, bool)
        assert isinstance(value, int)
        return cls(clicked, value)

    def __bool__(self):
        return self.clicked


def drag_int(
    label: str,
    value: int,
    change_speed=1.0,
    min_value=0,
    max_value=0,
    fmt="%d",
    flags: Union[SliderFlags, int] = 0,
):
    if isinstance(flags, SliderFlags):
        flags = int(flags)
    assert isinstance(flags, int)
    result = imgui.drag_int(
        label=label,
        v=value,
        v_speed=change_speed,
        v_min=min_value,
        v_max=max_value,
        format=fmt,
        flags=flags,
    )
    return DragIntResult.from_raw(result)
