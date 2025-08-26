# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.encoding.ascii import SPACE
from cvp.imgui.flags import color_var

_SINGLE_WIDTH_DUMMY_CHAR_ASCII: Final[str] = chr(SPACE)


def get_border_u32() -> int:
    color = imgui.get_style_color_vec4(color_var.BORDER)
    return imgui.get_color_u32(color)


def get_text_u32() -> int:
    color = imgui.get_style_color_vec4(color_var.TEXT)
    return imgui.get_color_u32(color)


def get_text_disabled_u32() -> int:
    color = imgui.get_style_color_vec4(color_var.TEXT_DISABLED)
    return imgui.get_color_u32(color)


def get_text_selected_bg_u32() -> int:
    color = imgui.get_style_color_vec4(color_var.TEXT_SELECTED_BG)
    return imgui.get_color_u32(color)


def get_text_link_u32() -> int:
    color = imgui.get_style_color_vec4(color_var.TEXT_LINK)
    return imgui.get_color_u32(color)


def get_border_width() -> float:
    return imgui.get_style().child_border_size


def get_item_spacing_x() -> float:
    return imgui.get_style().item_spacing.x


def get_item_spacing_y() -> float:
    return imgui.get_style().item_spacing.y


def get_item_spacing_x_half() -> float:
    return get_item_spacing_x() / 2.0


def get_item_spacing_y_half() -> float:
    return get_item_spacing_y() / 2.0


def get_text_line_height() -> float:
    return imgui.get_text_line_height()


def get_line_height() -> float:
    return get_text_line_height() + get_item_spacing_y_half()


def get_char_width() -> float:
    return imgui.calc_text_size(_SINGLE_WIDTH_DUMMY_CHAR_ASCII).x
