# -*- coding: utf-8 -*-

from typing import Optional, Type

from imgui_bundle import imgui

from cvp.config.sections.navigation import NavigationConfig, RecentItem
from cvp.imgui.menu_item import menu_item
from cvp.variables import STATIC_LABEL_CLEAR_RECENT_ITEMS_MENU


def menu_recent_items(
    label: str,
    config: NavigationConfig,
    cls: Type,
    *,
    suffix=None,
    append_clear_menu=False,
    no_reversed=False,
    clear_menu_label=STATIC_LABEL_CLEAR_RECENT_ITEMS_MENU,
) -> Optional[RecentItem]:
    recent_items = config.get_recent_items(cls, suffix=suffix)

    if imgui.begin_menu(label, enabled=bool(recent_items)):
        try:
            for item in reversed(recent_items) if not no_reversed else recent_items:
                if menu_item(item.value):
                    return item

            if append_clear_menu:
                imgui.separator()
                if menu_item(clear_menu_label):
                    config.clear_recent_items(cls, suffix=suffix)
        finally:
            imgui.end_menu()

    return None
