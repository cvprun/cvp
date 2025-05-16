# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class TabItemFlags(IntFlag):
    # fmt: off
    none = imgui.TabItemFlags_.none.value
    unsaved_document = imgui.TabItemFlags_.unsaved_document.value
    set_selected = imgui.TabItemFlags_.set_selected.value
    no_close_with_middle_mouse_button = imgui.TabItemFlags_.no_close_with_middle_mouse_button.value  # noqa: E501
    no_push_id = imgui.TabItemFlags_.no_push_id.value
    no_tooltip = imgui.TabItemFlags_.no_tooltip.value
    no_reorder = imgui.TabItemFlags_.no_reorder.value
    leading = imgui.TabItemFlags_.leading.value
    trailing = imgui.TabItemFlags_.trailing.value
    no_assumed_closure = imgui.TabItemFlags_.no_assumed_closure.value
    # fmt: on


# fmt: off
UNSAVED_DOCUMENT: Final[int] = int(TabItemFlags.unsaved_document)
SET_SELECTED: Final[int] = int(TabItemFlags.set_selected)
NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON: Final[int] = int(TabItemFlags.no_close_with_middle_mouse_button)  # noqa: E501
NO_PUSH_ID: Final[int] = int(TabItemFlags.no_push_id)
NO_TOOLTIP: Final[int] = int(TabItemFlags.no_tooltip)
NO_REORDER: Final[int] = int(TabItemFlags.no_reorder)
LEADING: Final[int] = int(TabItemFlags.leading)
TRAILING: Final[int] = int(TabItemFlags.trailing)
NO_ASSUMED_CLOSURE: Final[int] = int(TabItemFlags.no_assumed_closure)
# fmt: on


def merge_tab_item_flags(*flags: Union[TabItemFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))
