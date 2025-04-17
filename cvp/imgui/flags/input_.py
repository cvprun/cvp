# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class InputFlags(IntFlag):
    none = imgui.InputFlags_.none.value
    repeat = imgui.InputFlags_.repeat.value
    route_active = imgui.InputFlags_.route_active.value
    route_focused = imgui.InputFlags_.route_focused.value
    route_global = imgui.InputFlags_.route_global.value
    route_always = imgui.InputFlags_.route_always.value
    route_over_focused = imgui.InputFlags_.route_over_focused.value
    route_over_active = imgui.InputFlags_.route_over_active.value
    route_unless_bg_focused = imgui.InputFlags_.route_unless_bg_focused.value
    route_from_root_window = imgui.InputFlags_.route_from_root_window.value
    tooltip = imgui.InputFlags_.tooltip.value


NONE: Final[int] = int(InputFlags.none)
REPEAT: Final[int] = int(InputFlags.repeat)
ROUTE_ACTIVE: Final[int] = int(InputFlags.route_active)
ROUTE_FOCUSED: Final[int] = int(InputFlags.route_focused)
ROUTE_GLOBAL: Final[int] = int(InputFlags.route_global)
ROUTE_ALWAYS: Final[int] = int(InputFlags.route_always)
ROUTE_OVER_FOCUSED: Final[int] = int(InputFlags.route_over_focused)
ROUTE_OVER_ACTIVE: Final[int] = int(InputFlags.route_over_active)
ROUTE_UNLESS_BG_FOCUSED: Final[int] = int(InputFlags.route_unless_bg_focused)
ROUTE_FROM_ROOT_WINDOW: Final[int] = int(InputFlags.route_from_root_window)
TOOLTIP: Final[int] = int(InputFlags.tooltip)


def merge_input_flags(*flags: Union[InputFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))
