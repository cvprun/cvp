# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional, Union

from imgui_bundle import imgui

from cvp.imgui.flags.input_text import InputTextFlags
from cvp.imgui.get_fit_width_as_reverse import get_fit_width_as_reverse


class InputTextMultilineResult(NamedTuple):
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


def calc_input_text_multiline_height(value: str) -> float:
    frame_padding = imgui.get_style().frame_padding
    line_count = value.count("\n") + 1
    text_height = imgui.get_font_size() * line_count
    return text_height + (frame_padding.y * 2)


def input_text_multiline(
    label: str,
    value: str,
    flags: Union[InputTextFlags, int] = 0,
    size: Optional[imgui.ImVec2Like] = None,
):
    if isinstance(flags, InputTextFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    if size is None:
        width = get_fit_width_as_reverse()
        height = calc_input_text_multiline_height(value)
        size = imgui.ImVec2(width, height)
    assert size is not None

    raw_result = imgui.input_text_multiline(label, value, size, flags)
    return InputTextMultilineResult.from_raw(raw_result)
