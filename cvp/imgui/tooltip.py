# -*- coding: utf-8 -*-

from typing import Optional, Union

from imgui_bundle import imgui

from cvp.imgui.flags.hovered import HoveredFlags
from cvp.variables import HOVERED_TOOLTIP_TEXT_WRAPPED_WIDTH


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


def hovered_tooltip_text_wrapped(
    text: str,
    flags: Union[HoveredFlags, int] = 0,
    *,
    width: Optional[int] = HOVERED_TOOLTIP_TEXT_WRAPPED_WIDTH,
) -> bool:
    if isinstance(flags, HoveredFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    if imgui.is_item_hovered(flags):
        if imgui.begin_tooltip():
            try:
                use_text_wrap_pos = width is not None and 1 <= width
                if use_text_wrap_pos:
                    assert isinstance(width, int)
                    imgui.push_text_wrap_pos(imgui.get_cursor_pos_x() + width)
                imgui.text_wrapped(text)
                if use_text_wrap_pos:
                    imgui.pop_text_wrap_pos()
            finally:
                imgui.end_tooltip()
        return True
    else:
        return False
