# -*- coding: utf-8 -*-

from typing import Optional, Union

from imgui_bundle import imgui

from cvp.canvas.canvas import Canvas
from cvp.imgui.flags.mouse_button import MOUSE_LEFT, MouseButton
from cvp.imgui.flags.selectable import ALLOW_DOUBLE_CLICK, SelectableFlags
from cvp.imgui.selectable import SelectableResult, selectable


def selectable_canvas(
    canvas: Canvas,
    selected=False,
    flags: Union[SelectableFlags, int] = 0,
    size: Optional[imgui.ImVec2Like] = None,
    *,
    use_double_clicked=False,
    double_click_button: Union[MouseButton, int] = MOUSE_LEFT,
):
    if isinstance(flags, SelectableFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    if use_double_clicked:
        flags |= ALLOW_DOUBLE_CLICK

    name = str(canvas.name) if canvas.name else Canvas.__name__
    label = f"{name}###{canvas.uuid}"
    result = selectable(label, selected, flags, size)

    if result.clicked and use_double_clicked:
        if isinstance(double_click_button, MouseButton):
            double_click_button = int(double_click_button)
        assert isinstance(double_click_button, int)

        clicked = imgui.is_mouse_double_clicked(double_click_button)
        result = SelectableResult(clicked, result.selected)

    return result
