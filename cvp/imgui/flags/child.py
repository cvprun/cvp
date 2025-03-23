# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class ChildFlags(IntFlag):
    none = imgui.ChildFlags_.none.value
    borders = imgui.ChildFlags_.borders.value
    always_use_window_padding = imgui.ChildFlags_.always_use_window_padding.value
    resize_x = imgui.ChildFlags_.resize_x.value
    resize_y = imgui.ChildFlags_.resize_y.value
    auto_resize_x = imgui.ChildFlags_.auto_resize_x.value
    auto_resize_y = imgui.ChildFlags_.auto_resize_y.value
    always_auto_resize = imgui.ChildFlags_.always_auto_resize.value
    frame_style = imgui.ChildFlags_.frame_style.value
    nav_flattened = imgui.ChildFlags_.nav_flattened.value


NONE: Final[int] = int(ChildFlags.none)
BORDERS: Final[int] = int(ChildFlags.borders)
ALWAYS_USE_WINDOW_PADDING: Final[int] = int(ChildFlags.always_use_window_padding)
RESIZE_X: Final[int] = int(ChildFlags.resize_x)
RESIZE_Y: Final[int] = int(ChildFlags.resize_y)
AUTO_RESIZE_X: Final[int] = int(ChildFlags.auto_resize_x)
AUTO_RESIZE_Y: Final[int] = int(ChildFlags.auto_resize_y)
ALWAYS_AUTO_RESIZE: Final[int] = int(ChildFlags.always_auto_resize)
FRAME_STYLE: Final[int] = int(ChildFlags.frame_style)
NAV_FLATTENED: Final[int] = int(ChildFlags.nav_flattened)


def merge_child_flags(*flags: Union[ChildFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))
