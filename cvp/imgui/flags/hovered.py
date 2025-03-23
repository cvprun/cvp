# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class HoveredFlags(IntFlag):
    # fmt: off
    none = imgui.HoveredFlags_.none.value
    child_windows = imgui.HoveredFlags_.child_windows.value
    root_window = imgui.HoveredFlags_.root_window.value
    any_window = imgui.HoveredFlags_.any_window.value
    no_popup_hierarchy = imgui.HoveredFlags_.no_popup_hierarchy.value
    dock_hierarchy = imgui.HoveredFlags_.dock_hierarchy.value
    allow_when_blocked_by_popup = imgui.HoveredFlags_.allow_when_blocked_by_popup.value
    allow_when_blocked_by_active_item = imgui.HoveredFlags_.allow_when_blocked_by_active_item.value  # noqa: E501
    allow_when_overlapped_by_item = imgui.HoveredFlags_.allow_when_overlapped_by_item.value  # noqa: E501
    allow_when_overlapped_by_window = imgui.HoveredFlags_.allow_when_overlapped_by_window.value  # noqa: E501
    allow_when_disabled = imgui.HoveredFlags_.allow_when_disabled.value
    no_nav_override = imgui.HoveredFlags_.no_nav_override.value
    allow_when_overlapped = imgui.HoveredFlags_.allow_when_overlapped.value
    rect_only = imgui.HoveredFlags_.rect_only.value
    root_and_child_windows = imgui.HoveredFlags_.root_and_child_windows.value
    for_tooltip = imgui.HoveredFlags_.for_tooltip.value
    stationary = imgui.HoveredFlags_.stationary.value
    delay_none = imgui.HoveredFlags_.delay_none.value
    delay_short = imgui.HoveredFlags_.delay_short.value
    delay_normal = imgui.HoveredFlags_.delay_normal.value
    no_shared_delay = imgui.HoveredFlags_.no_shared_delay.value
    # fmt: on


# fmt: off
NONE: Final[int] = int(HoveredFlags.none)
CHILD_WINDOWS: Final[int] = int(HoveredFlags.child_windows)
ROOT_WINDOW: Final[int] = int(HoveredFlags.root_window)
ANY_WINDOW: Final[int] = int(HoveredFlags.any_window)
NO_POPUP_HIERARCHY: Final[int] = int(HoveredFlags.no_popup_hierarchy)
DOCK_HIERARCHY: Final[int] = int(HoveredFlags.dock_hierarchy)
ALLOW_WHEN_BLOCKED_BY_POPUP: Final[int] = int(HoveredFlags.allow_when_blocked_by_popup)
ALLOW_WHEN_BLOCKED_BY_ACTIVE_ITEM: Final[int] = int(HoveredFlags.allow_when_blocked_by_active_item)  # noqa: E501
ALLOW_WHEN_OVERLAPPED_BY_ITEM: Final[int] = int(HoveredFlags.allow_when_overlapped_by_item)  # noqa: E501
ALLOW_WHEN_OVERLAPPED_BY_WINDOW: Final[int] = int(HoveredFlags.allow_when_overlapped_by_window)  # noqa: E501
ALLOW_WHEN_DISABLED: Final[int] = int(HoveredFlags.allow_when_disabled)
NO_NAV_OVERRIDE: Final[int] = int(HoveredFlags.no_nav_override)
ALLOW_WHEN_OVERLAPPED: Final[int] = int(HoveredFlags.allow_when_overlapped)
RECT_ONLY: Final[int] = int(HoveredFlags.rect_only)
ROOT_AND_CHILD_WINDOWS: Final[int] = int(HoveredFlags.root_and_child_windows)
FOR_TOOLTIP: Final[int] = int(HoveredFlags.for_tooltip)
STATIONARY: Final[int] = int(HoveredFlags.stationary)
DELAY_NONE: Final[int] = int(HoveredFlags.delay_none)
DELAY_SHORT: Final[int] = int(HoveredFlags.delay_short)
DELAY_NORMAL: Final[int] = int(HoveredFlags.delay_normal)
NO_SHARED_DELAY: Final[int] = int(HoveredFlags.no_shared_delay)
# fmt: on


def merge_focused_flags(*flags: Union[HoveredFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))
