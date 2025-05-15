# -*- coding: utf-8 -*-

from typing import Final, Optional, Type

from imgui_bundle import imgui

from cvp.config.sections.navigation import NavigationConfig, RecentItem
from cvp.imgui.menu_item import menu_item

CLEAR_RECENT_ITEMS_MENU_LABEL: Final[str] = "Clear recent items"


def menu_recent_items(
    label: str,
    config: NavigationConfig,
    cls: Type,
    *,
    suffix=None,
    append_clear_menu=False,
    clear_menu_label=CLEAR_RECENT_ITEMS_MENU_LABEL,
) -> Optional[RecentItem]:
    recent_items = config.get_recent_items(cls, suffix=suffix)

    if imgui.begin_menu(label, enabled=bool(recent_items)):
        try:
            for item in recent_items:
                if menu_item(item.value):
                    return item

            if append_clear_menu:
                imgui.separator()
                if menu_item(clear_menu_label):
                    config.clear_recent_items(cls, suffix=suffix)
        finally:
            imgui.end_menu()

    return None
