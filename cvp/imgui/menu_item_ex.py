# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional

from imgui_bundle import imgui


class MenuItemResult(NamedTuple):
    clicked: bool
    state: bool

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        clicked = result[0]
        state = result[1]
        assert isinstance(clicked, bool)
        assert isinstance(state, bool)
        return cls(clicked, state)

    def __bool__(self):
        return self.clicked


def menu_item(
    label: str,
    selected=False,
    shortcut: Optional[str] = None,
    enabled=True,
):
    result = imgui.menu_item(label, shortcut, selected, enabled)
    return MenuItemResult.from_raw(result)
