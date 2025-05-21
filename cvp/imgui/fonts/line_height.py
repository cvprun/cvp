# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def get_line_height() -> float:
    font_height = imgui.get_font_size()
    line_gap = imgui.get_style().item_spacing.y
    return font_height + line_gap
