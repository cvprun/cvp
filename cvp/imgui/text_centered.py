# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def text_centered(text: str) -> None:
    window_size = imgui.get_window_size()
    text_size = imgui.calc_text_size(text)
    text_x = (window_size.x - text_size.x) * 0.5
    text_y = (window_size.y - text_size.y) * 0.5
    imgui.set_cursor_pos((text_x, text_y))
    imgui.text(text)
