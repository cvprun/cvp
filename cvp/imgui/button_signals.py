# -*- coding: utf-8 -*-

from signal import Signals
from typing import Optional

from imgui_bundle import imgui

from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button_enum_wrapped import button_enum_wrapped
from cvp.imgui.flags.child import AUTO_RESIZE_Y, BORDERS
from cvp.imgui.flags.style_var import ITEM_SPACING


def button_signals(
    label: str,
    width: Optional[float] = None,
    *,
    top_title: Optional[str] = None,
    right_title: Optional[str] = None,
    border=False,
    debugging=False,
) -> Optional[int]:
    if width is None:
        width = imgui.calc_item_width()
    assert isinstance(width, float)

    with begin_child_context(
        label=label,
        size=(width, 0),
        child_flags=AUTO_RESIZE_Y | (BORDERS if border else 0),
    ):
        if top_title:
            imgui.text(top_title)
            imgui.separator()

        imgui.push_style_var_x(ITEM_SPACING, 1.0)
        try:
            clicked_index = button_enum_wrapped(Signals, show_debugging=debugging)
        finally:
            imgui.pop_style_var()

        if clicked_index is not None:
            return int(list(Signals)[clicked_index].value)

    if right_title:
        imgui.same_line(spacing=imgui.get_style().item_inner_spacing.x)
        imgui.text(right_title)

    return None
