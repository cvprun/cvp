# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def calc_right_align_pos_x(text: str) -> float:
    window_width = imgui.get_window_width()
    text_width = imgui.calc_text_size(text).x
    item_spacing_x = imgui.get_style().item_spacing.x
    return window_width - text_width - item_spacing_x


def set_cursor_pos_for_text_right_align(text: str) -> None:
    imgui.set_cursor_pos_x(calc_right_align_pos_x(text))


def text_right_align(text: str) -> None:
    set_cursor_pos_for_text_right_align(text)
    imgui.text(text)


def text_disabled_right_align(text: str) -> None:
    set_cursor_pos_for_text_right_align(text)
    imgui.text_disabled(text)
