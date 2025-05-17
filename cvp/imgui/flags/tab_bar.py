# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class TabBarFlags(IntFlag):
    # fmt: off
    none = imgui.TabBarFlags_.none.value
    reorderable = imgui.TabBarFlags_.reorderable.value
    auto_select_new_tabs = imgui.TabBarFlags_.auto_select_new_tabs.value
    tab_list_popup_button = imgui.TabBarFlags_.tab_list_popup_button.value
    no_close_with_middle_mouse_button = imgui.TabBarFlags_.no_close_with_middle_mouse_button.value  # noqa: E501
    no_tab_list_scrolling_buttons = imgui.TabBarFlags_.no_tab_list_scrolling_buttons.value  # noqa: E501
    no_tooltip = imgui.TabBarFlags_.no_tooltip.value
    draw_selected_overline = imgui.TabBarFlags_.draw_selected_overline.value
    fitting_policy_resize_down = imgui.TabBarFlags_.fitting_policy_resize_down.value
    fitting_policy_scroll = imgui.TabBarFlags_.fitting_policy_scroll.value
    # fmt: on


# fmt: off
NONE: Final[int] = int(TabBarFlags.none)
REORDERABLE: Final[int] = int(TabBarFlags.reorderable)
AUTO_SELECT_NEW_TABS: Final[int] = int(TabBarFlags.auto_select_new_tabs)
TAB_LIST_POPUP_BUTTON: Final[int] = int(TabBarFlags.tab_list_popup_button)
NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON: Final[int] = int(TabBarFlags.no_close_with_middle_mouse_button)  # noqa: E501
NO_TAB_LIST_SCROLLING_BUTTONS: Final[int] = int(TabBarFlags.no_tab_list_scrolling_buttons)  # noqa: E501
NO_TOOLTIP: Final[int] = int(TabBarFlags.no_tooltip)
DRAW_SELECTED_OVERLINE: Final[int] = int(TabBarFlags.draw_selected_overline)
FITTING_POLICY_RESIZE_DOWN: Final[int] = int(TabBarFlags.fitting_policy_resize_down)
FITTING_POLICY_SCROLL: Final[int] = int(TabBarFlags.fitting_policy_scroll)
# fmt: on


def merge_tab_bar_flags(*flags: Union[TabBarFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))
