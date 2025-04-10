# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def footer_height_as_reverse() -> float:
    """
    Reserve enough left-over height for 1 separator + 1 input text
    """

    frame_spacing = imgui.get_frame_height_with_spacing()
    item_spacing = imgui.get_style().item_spacing.y
    return -1 * (frame_spacing + item_spacing)
