# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class FocusedFlags(IntFlag):
    none = imgui.FocusedFlags_.none.value
    child_windows = imgui.FocusedFlags_.child_windows.value
    root_window = imgui.FocusedFlags_.root_window.value
    any_window = imgui.FocusedFlags_.any_window.value
    no_popup_hierarchy = imgui.FocusedFlags_.no_popup_hierarchy.value
    dock_hierarchy = imgui.FocusedFlags_.dock_hierarchy.value
    root_and_child_windows = imgui.FocusedFlags_.root_and_child_windows.value


NONE: Final[int] = int(FocusedFlags.none)
CHILD_WINDOWS: Final[int] = int(FocusedFlags.child_windows)
ROOT_WINDOW: Final[int] = int(FocusedFlags.root_window)
ANY_WINDOW: Final[int] = int(FocusedFlags.any_window)
NO_POPUP_HIERARCHY: Final[int] = int(FocusedFlags.no_popup_hierarchy)
DOCK_HIERARCHY: Final[int] = int(FocusedFlags.dock_hierarchy)
ROOT_AND_CHILD_WINDOWS: Final[int] = int(FocusedFlags.root_and_child_windows)


def merge_focused_flags(*flags: Union[FocusedFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))
