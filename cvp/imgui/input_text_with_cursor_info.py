# -*- coding: utf-8 -*-

from dataclasses import dataclass
from functools import partial
from typing import NamedTuple, Union

from imgui_bundle import imgui

from cvp.imgui.flags.input_text import (
    CALLBACK_ALWAYS,
    InputTextFlags,
    merge_input_text_flags,
)
from cvp.imgui.input_text import input_text
from cvp.variables import NOT_FOUND_INDEX


@dataclass
class CursorInfoResult:
    cursor_pos: int = NOT_FOUND_INDEX
    selection_start: int = NOT_FOUND_INDEX
    selection_end: int = NOT_FOUND_INDEX


class InputTextWithCursorInfoResult(NamedTuple):
    changed: bool
    value: str
    cursor_pos: int
    selection_start: int
    selection_end: int

    def __bool__(self):
        return self.changed


def _input_text_callback(
    data: imgui.InputTextCallbackData,
    *,
    user_data: CursorInfoResult,
) -> int:
    assert data.flags & CALLBACK_ALWAYS
    assert isinstance(user_data, CursorInfoResult)
    user_data.cursor_pos = data.cursor_pos
    user_data.selection_start = data.selection_start
    user_data.selection_end = data.selection_end
    return 0


def input_text_with_cursor_info(
    label: str,
    value: str,
    flags: Union[InputTextFlags, int] = 0,
):
    info = CursorInfoResult()
    result = input_text(
        label,
        value,
        merge_input_text_flags(flags, CALLBACK_ALWAYS),
        partial(_input_text_callback, user_data=info),
    )
    return InputTextWithCursorInfoResult(
        result.changed,
        result.value,
        info.cursor_pos,
        info.selection_start,
        info.selection_end,
    )
