# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def set_window_min_size(min_width: int, min_height: int) -> None:
    size = imgui.get_window_size()
    cw = size.x
    ch = size.y
    w = cw if cw >= min_width else min_width
    h = ch if ch >= min_height else min_height
    imgui.set_window_size((w, h))
