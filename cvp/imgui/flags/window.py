# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class WindowFlags(IntFlag):
    none = imgui.WindowFlags_.none.value
    no_title_bar = imgui.WindowFlags_.no_title_bar.value
    no_resize = imgui.WindowFlags_.no_resize.value
    no_move = imgui.WindowFlags_.no_move.value
    no_scrollbar = imgui.WindowFlags_.no_scrollbar.value
    no_scroll_with_mouse = imgui.WindowFlags_.no_scroll_with_mouse.value
    no_collapse = imgui.WindowFlags_.no_collapse.value
    always_auto_resize = imgui.WindowFlags_.always_auto_resize.value
    no_background = imgui.WindowFlags_.no_background.value
    no_saved_settings = imgui.WindowFlags_.no_saved_settings.value
    no_mouse_inputs = imgui.WindowFlags_.no_mouse_inputs.value
    menu_bar = imgui.WindowFlags_.menu_bar.value
    horizontal_scrollbar = imgui.WindowFlags_.horizontal_scrollbar.value
    no_focus_on_appearing = imgui.WindowFlags_.no_focus_on_appearing.value
    no_bring_to_front_on_focus = imgui.WindowFlags_.no_bring_to_front_on_focus.value
    always_vertical_scrollbar = imgui.WindowFlags_.always_vertical_scrollbar.value
    always_horizontal_scrollbar = imgui.WindowFlags_.always_horizontal_scrollbar.value
    no_nav_inputs = imgui.WindowFlags_.no_nav_inputs.value
    no_nav_focus = imgui.WindowFlags_.no_nav_focus.value
    unsaved_document = imgui.WindowFlags_.unsaved_document.value
    no_docking = imgui.WindowFlags_.no_docking.value
    no_nav = imgui.WindowFlags_.no_nav.value
    no_decoration = imgui.WindowFlags_.no_decoration.value
    no_inputs = imgui.WindowFlags_.no_inputs.value

    # [Internal]
    _child_window = imgui.WindowFlags_.child_window.value
    _tooltip = imgui.WindowFlags_.tooltip.value
    _popup = imgui.WindowFlags_.popup.value
    _modal = imgui.WindowFlags_.modal.value
    _child_menu = imgui.WindowFlags_.child_menu.value
    _dock_node_host = imgui.WindowFlags_.dock_node_host.value


NONE: Final[int] = int(WindowFlags.none)
NO_TITLE_BAR: Final[int] = int(WindowFlags.no_title_bar)
NO_RESIZE: Final[int] = int(WindowFlags.no_resize)
NO_MOVE: Final[int] = int(WindowFlags.no_move)
NO_SCROLLBAR: Final[int] = int(WindowFlags.no_scrollbar)
NO_SCROLL_WITH_MOUSE: Final[int] = int(WindowFlags.no_scroll_with_mouse)
NO_COLLAPSE: Final[int] = int(WindowFlags.no_collapse)
ALWAYS_AUTO_RESIZE: Final[int] = int(WindowFlags.always_auto_resize)
NO_BACKGROUND: Final[int] = int(WindowFlags.no_background)
NO_SAVED_SETTINGS: Final[int] = int(WindowFlags.no_saved_settings)
NO_MOUSE_INPUTS: Final[int] = int(WindowFlags.no_mouse_inputs)
MENU_BAR: Final[int] = int(WindowFlags.menu_bar)
HORIZONTAL_SCROLLBAR: Final[int] = int(WindowFlags.horizontal_scrollbar)
NO_FOCUS_ON_APPEARING: Final[int] = int(WindowFlags.no_focus_on_appearing)
NO_BRING_TO_FRONT_ON_FOCUS: Final[int] = int(WindowFlags.no_bring_to_front_on_focus)
ALWAYS_VERTICAL_SCROLLBAR: Final[int] = int(WindowFlags.always_vertical_scrollbar)
ALWAYS_HORIZONTAL_SCROLLBAR: Final[int] = int(WindowFlags.always_horizontal_scrollbar)
NO_NAV_INPUTS: Final[int] = int(WindowFlags.no_nav_inputs)
NO_NAV_FOCUS: Final[int] = int(WindowFlags.no_nav_focus)
UNSAVED_DOCUMENT: Final[int] = int(WindowFlags.unsaved_document)
NO_DOCKING: Final[int] = int(WindowFlags.no_docking)
NO_NAV: Final[int] = int(WindowFlags.no_nav)
NO_DECORATION: Final[int] = int(WindowFlags.no_decoration)
NO_INPUTS: Final[int] = int(WindowFlags.no_inputs)


def merge_window_flags(*flags: Union[WindowFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))


BACKGROUND_FLAGS: Final[int] = merge_window_flags(
    WindowFlags.no_decoration,
    WindowFlags.no_saved_settings,
    WindowFlags.no_focus_on_appearing,
    WindowFlags.no_bring_to_front_on_focus,
    WindowFlags.no_nav,
    WindowFlags.no_move,
)

CANVAS_FLAGS: Final[int] = merge_window_flags(
    WindowFlags.no_resize,
    WindowFlags.no_move,
    WindowFlags.no_scrollbar,
)

OVERLAY_WINDOW_FLAGS: Final[int] = merge_window_flags(
    WindowFlags.no_decoration,
    WindowFlags.always_auto_resize,
    WindowFlags.no_saved_settings,
    WindowFlags.no_nav,
    WindowFlags.no_move,
)

TOAST_WINDOW_FLAGS: Final[int] = merge_window_flags(
    WindowFlags.no_decoration,
    WindowFlags.always_auto_resize,
    WindowFlags.no_saved_settings,
    WindowFlags.no_move,
    WindowFlags.no_nav,
    WindowFlags.unsaved_document,
    WindowFlags.no_bring_to_front_on_focus,
    WindowFlags.no_focus_on_appearing,
    WindowFlags.no_inputs,
)

