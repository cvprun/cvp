# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.imgui.flags.window import BACKGROUND_FLAGS


def begin_background(label: str):
    viewport = imgui.get_main_viewport()
    wx, wy = viewport.work_pos
    ww, wh = viewport.work_size
    imgui.set_next_window_pos((wx, wy))
    imgui.set_next_window_size(ww, wh)

    imgui.push_style_var(imgui.StyleVar_.window_border_size.value, 0.0)
    imgui.push_style_var(imgui.StyleVar_.window_padding.value, (0, 0))
    result = imgui.begin(label, False, BACKGROUND_FLAGS)
    imgui.pop_style_var(2)
    return result


def end_background() -> None:
    imgui.end()
