# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class ColorEditFlags(IntFlag):
    none = imgui.ColorEditFlags_.none.value
    no_alpha = imgui.ColorEditFlags_.no_alpha.value
    no_picker = imgui.ColorEditFlags_.no_picker.value
    no_options = imgui.ColorEditFlags_.no_options.value
    no_small_preview = imgui.ColorEditFlags_.no_small_preview.value
    no_inputs = imgui.ColorEditFlags_.no_inputs.value
    no_tooltip = imgui.ColorEditFlags_.no_tooltip.value
    no_label = imgui.ColorEditFlags_.no_label.value
    no_side_preview = imgui.ColorEditFlags_.no_side_preview.value
    no_drag_drop = imgui.ColorEditFlags_.no_drag_drop.value
    no_border = imgui.ColorEditFlags_.no_border.value

    # User Options
    alpha_bar = imgui.ColorEditFlags_.alpha_bar.value
    alpha_preview = imgui.ColorEditFlags_.alpha_preview.value
    alpha_preview_half = imgui.ColorEditFlags_.alpha_preview_half.value
    hdr = imgui.ColorEditFlags_.hdr.value
    display_rgb = imgui.ColorEditFlags_.display_rgb.value
    display_hsv = imgui.ColorEditFlags_.display_hsv.value
    display_hex = imgui.ColorEditFlags_.display_hex.value
    uint8 = imgui.ColorEditFlags_.uint8.value
    float = imgui.ColorEditFlags_.float.value
    picker_hue_bar = imgui.ColorEditFlags_.picker_hue_bar.value
    picker_hue_wheel = imgui.ColorEditFlags_.picker_hue_wheel.value
    input_rgb = imgui.ColorEditFlags_.input_rgb.value
    input_hsv = imgui.ColorEditFlags_.input_hsv.value

    # Defaults Options.
    default_options_ = imgui.ColorEditFlags_.default_options_.value

    # [Internal] Masks
    display_mask_ = imgui.ColorEditFlags_.display_mask_.value
    data_type_mask_ = imgui.ColorEditFlags_.data_type_mask_.value
    picker_mask_ = imgui.ColorEditFlags_.picker_mask_.value
    input_mask_ = imgui.ColorEditFlags_.input_mask_.value

    # Obsolete names
    # ImGuiColorEditFlags_RGB


NONE: Final[int] = int(ColorEditFlags.none)
NO_ALPHA: Final[int] = int(ColorEditFlags.no_alpha)
NO_PICKER: Final[int] = int(ColorEditFlags.no_picker)
NO_OPTIONS: Final[int] = int(ColorEditFlags.no_options)
NO_SMALL_PREVIEW: Final[int] = int(ColorEditFlags.no_small_preview)
NO_INPUTS: Final[int] = int(ColorEditFlags.no_inputs)
NO_TOOLTIP: Final[int] = int(ColorEditFlags.no_tooltip)
NO_LABEL: Final[int] = int(ColorEditFlags.no_label)
NO_SIDE_PREVIEW: Final[int] = int(ColorEditFlags.no_side_preview)
NO_DRAG_DROP: Final[int] = int(ColorEditFlags.no_drag_drop)
NO_BORDER: Final[int] = int(ColorEditFlags.no_border)
ALPHA_BAR: Final[int] = int(ColorEditFlags.alpha_bar)
ALPHA_PREVIEW: Final[int] = int(ColorEditFlags.alpha_preview)
ALPHA_PREVIEW_HALF: Final[int] = int(ColorEditFlags.alpha_preview_half)
HDR: Final[int] = int(ColorEditFlags.hdr)
DISPLAY_RGB: Final[int] = int(ColorEditFlags.display_rgb)
DISPLAY_HSV: Final[int] = int(ColorEditFlags.display_hsv)
DISPLAY_HEX: Final[int] = int(ColorEditFlags.display_hex)
UINT8: Final[int] = int(ColorEditFlags.uint8)
FLOAT: Final[int] = int(ColorEditFlags.float)
PICKER_HUE_BAR: Final[int] = int(ColorEditFlags.picker_hue_bar)
PICKER_HUE_WHEEL: Final[int] = int(ColorEditFlags.picker_hue_wheel)
INPUT_RGB: Final[int] = int(ColorEditFlags.input_rgb)
INPUT_HSV: Final[int] = int(ColorEditFlags.input_hsv)


def merge_color_edit_flags(*flags: Union[ColorEditFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))
