# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def set_window_min_size(min_width: int, min_height: int) -> None:
    cw, ch = imgui.get_window_size()
    w = cw if cw >= min_width else min_width
    h = ch if ch >= min_height else min_height
    imgui.set_window_size(w, h)
