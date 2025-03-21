# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

BACKGROUND_WINDOW_FLAGS: Final[int] = (
    imgui.WINDOW_NO_DECORATION
    | imgui.WINDOW_NO_SAVED_SETTINGS
    | imgui.WINDOW_NO_FOCUS_ON_APPEARING
    | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS
    | imgui.WINDOW_NO_NAV
    | imgui.WINDOW_NO_MOVE
)


def begin_background(label: str):
    viewport = imgui.get_main_viewport()
    wx, wy = viewport.work_pos
    ww, wh = viewport.work_size
    imgui.set_next_window_position(wx, wy)
    imgui.set_next_window_size(ww, wh)

    imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0.0)
    imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
    result = imgui.begin(label, False, BACKGROUND_WINDOW_FLAGS)
    imgui.pop_style_var(2)
    return result


def end_background() -> None:
    imgui.end()
