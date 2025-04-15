# -*- coding: utf-8 -*-

from typing import Union

from imgui_bundle import imgui

from cvp.imgui.flags.hovered import HoveredFlags


def hovered_tooltip_text(text: str, flags: Union[HoveredFlags, int] = 0) -> bool:
    if isinstance(flags, HoveredFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    if imgui.is_item_hovered(flags):
        if imgui.begin_tooltip():
            try:
                imgui.text(text)
            finally:
                imgui.end_tooltip()
        return True
    else:
        return False
