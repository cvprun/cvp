# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def calc_button_size(text: str) -> imgui.ImVec2:
    text_size = imgui.calc_text_size(text, None, hide_text_after_double_hash=True)

    frame_padding = imgui.get_style().frame_padding
    padding_width = frame_padding.x * 2.0  # Left and Right Padding
    padding_height = frame_padding.y * 2.0  # Top and Bottom Padding

    width = text_size.x + padding_width
    height = text_size.y + padding_height

    return imgui.ImVec2(width, height)
