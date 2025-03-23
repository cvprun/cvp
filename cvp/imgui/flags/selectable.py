# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final

from imgui_bundle import imgui


@unique
class SelectableFlags(IntFlag):
    none = imgui.SelectableFlags_.none.value
    no_auto_close_popups = imgui.SelectableFlags_.no_auto_close_popups.value
    span_all_columns = imgui.SelectableFlags_.span_all_columns.value
    allow_double_click = imgui.SelectableFlags_.allow_double_click.value
    disabled = imgui.SelectableFlags_.disabled.value
    allow_overlap = imgui.SelectableFlags_.allow_overlap.value
    highlight = imgui.SelectableFlags_.highlight.value


NONE: Final[int] = int(SelectableFlags.none)
NO_AUTO_CLOSE_POPUPS: Final[int] = int(SelectableFlags.no_auto_close_popups)
SPAN_ALL_COLUMNS: Final[int] = int(SelectableFlags.span_all_columns)
ALLOW_DOUBLE_CLICK: Final[int] = int(SelectableFlags.allow_double_click)
DISABLED: Final[int] = int(SelectableFlags.disabled)
ALLOW_OVERLAP: Final[int] = int(SelectableFlags.allow_overlap)
HIGHLIGHT: Final[int] = int(SelectableFlags.highlight)


def merge_selectable_flags(*flags: SelectableFlags) -> int:
    return int(reduce(lambda x, y: x | y, flags))
