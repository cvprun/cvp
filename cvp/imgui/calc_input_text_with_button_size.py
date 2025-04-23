# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def calc_input_multiline_text_size(input_value: str, button_label: str) -> imgui.ImVec2:
    """
    Calculate the size of "INPUT TEXT" leaving just enough space
    on the right for a single button.
    """

    # +----------------------------------------------------------+
    # |  CHILD WINDOW                                            |
    # |                                                          |
    # |  +----------------------------------------+  +--------+  |
    # |  | INPUT TEXT                             |  | BUTTON |  |
    # |  +----------------------------------------+  +--------+  |
    # |                                                          |
    # +----------------------------------------------------------+

    button_size = imgui.calc_text_size(button_label)
    button_width = button_size.x

    frame_padding = imgui.get_style().frame_padding
    item_spacing = imgui.get_style().item_spacing

    input_text_right = button_width + (frame_padding.x * 2) + item_spacing.x
    width = -1 * input_text_right

    line_count = input_value.count("\n") + 1
    text_height = imgui.get_font_size() * line_count
    height = text_height + (frame_padding.y * 2)

    return imgui.ImVec2(width, height)


def calc_input_text_width(button_label: str) -> float:
    return calc_input_multiline_text_size(str(), button_label).x
