# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final

from imgui_bundle import imgui


@unique
class InputTextFlags(IntFlag):
    none = imgui.InputTextFlags_.none.value
    chars_decimal = imgui.InputTextFlags_.chars_decimal.value
    chars_hexadecimal = imgui.InputTextFlags_.chars_hexadecimal.value
    chars_scientific = imgui.InputTextFlags_.chars_scientific.value
    chars_uppercase = imgui.InputTextFlags_.chars_uppercase.value
    chars_no_blank = imgui.InputTextFlags_.chars_no_blank.value

    # Inputs
    allow_tab_input = imgui.InputTextFlags_.allow_tab_input.value
    enter_returns_true = imgui.InputTextFlags_.enter_returns_true.value
    escape_clears_all = imgui.InputTextFlags_.escape_clears_all.value
    ctrl_enter_for_new_line = imgui.InputTextFlags_.ctrl_enter_for_new_line.value

    # Other options
    read_only = imgui.InputTextFlags_.read_only.value
    password = imgui.InputTextFlags_.password.value
    always_overwrite = imgui.InputTextFlags_.always_overwrite.value
    auto_select_all = imgui.InputTextFlags_.auto_select_all.value
    parse_empty_ref_val = imgui.InputTextFlags_.parse_empty_ref_val.value
    display_empty_ref_val = imgui.InputTextFlags_.display_empty_ref_val.value
    no_horizontal_scroll = imgui.InputTextFlags_.no_horizontal_scroll.value
    no_undo_redo = imgui.InputTextFlags_.no_undo_redo.value

    # Elide display / Alignment
    elide_left = imgui.InputTextFlags_.elide_left.value

    # Callback features
    callback_completion = imgui.InputTextFlags_.callback_completion.value
    callback_history = imgui.InputTextFlags_.callback_history.value
    callback_always = imgui.InputTextFlags_.callback_always.value
    callback_char_filter = imgui.InputTextFlags_.callback_char_filter.value
    callback_resize = imgui.InputTextFlags_.callback_resize.value
    callback_edit = imgui.InputTextFlags_.callback_edit.value

    # always_insert_mode


NONE: Final[int] = int(InputTextFlags.none)
CHARS_DECIMAL: Final[int] = int(InputTextFlags.chars_decimal)
CHARS_HEXADECIMAL: Final[int] = int(InputTextFlags.chars_hexadecimal)
CHARS_SCIENTIFIC: Final[int] = int(InputTextFlags.chars_scientific)
CHARS_UPPERCASE: Final[int] = int(InputTextFlags.chars_uppercase)
CHARS_NO_BLANK: Final[int] = int(InputTextFlags.chars_no_blank)
ALLOW_TAB_INPUT: Final[int] = int(InputTextFlags.allow_tab_input)
ENTER_RETURNS_TRUE: Final[int] = int(InputTextFlags.enter_returns_true)
ESCAPE_CLEARS_ALL: Final[int] = int(InputTextFlags.escape_clears_all)
CTRL_ENTER_FOR_NEW_LINE: Final[int] = int(InputTextFlags.ctrl_enter_for_new_line)
READ_ONLY: Final[int] = int(InputTextFlags.read_only)
PASSWORD: Final[int] = int(InputTextFlags.password)
ALWAYS_OVERWRITE: Final[int] = int(InputTextFlags.always_overwrite)
AUTO_SELECT_ALL: Final[int] = int(InputTextFlags.auto_select_all)
PARSE_EMPTY_REF_VAL: Final[int] = int(InputTextFlags.parse_empty_ref_val)
DISPLAY_EMPTY_REF_VAL: Final[int] = int(InputTextFlags.display_empty_ref_val)
NO_HORIZONTAL_SCROLL: Final[int] = int(InputTextFlags.no_horizontal_scroll)
NO_UNDO_REDO: Final[int] = int(InputTextFlags.no_undo_redo)
ELIDE_LEFT: Final[int] = int(InputTextFlags.elide_left)
CALLBACK_COMPLETION: Final[int] = int(InputTextFlags.callback_completion)
CALLBACK_HISTORY: Final[int] = int(InputTextFlags.callback_history)
CALLBACK_ALWAYS: Final[int] = int(InputTextFlags.callback_always)
CALLBACK_CHAR_FILTER: Final[int] = int(InputTextFlags.callback_char_filter)
CALLBACK_RESIZE: Final[int] = int(InputTextFlags.callback_resize)
CALLBACK_EDIT: Final[int] = int(InputTextFlags.callback_edit)


def merge_input_text_flags(*flags: InputTextFlags) -> int:
    return int(reduce(lambda x, y: x | y, flags))
