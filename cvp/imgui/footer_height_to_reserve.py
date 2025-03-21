# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def footer_height_to_reserve() -> int:
    """
    Reserve enough left-over height for 1 separator + 1 input text
    """
    return imgui.get_frame_height_with_spacing() + imgui.get_style().item_spacing.y
