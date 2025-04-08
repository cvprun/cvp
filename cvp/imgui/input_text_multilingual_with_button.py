# -*- coding: utf-8 -*-

from typing import Optional, Tuple, Union

from imgui_bundle import imgui

from cvp.imgui.flags.input_text import InputTextFlags
from cvp.imgui.input_text_multilingual import (
    InputTextMultilingualResult,
    input_text_multilingual,
)


def input_text_multilingual_with_button(
    label: str,
    value: str,
    button_label: str,
    input_flags: Union[InputTextFlags, int] = 0,
    input_size: Optional[imgui.ImVec2Like] = None,
    input_hint: Optional[str] = None,
) -> Tuple[InputTextMultilingualResult, bool]:
    button_label_size = imgui.calc_text_size(button_label)
    button_label_width = button_label_size.x
    frame_padding = imgui.get_style().frame_padding
    frame_padding_x = frame_padding.x
    item_spacing = imgui.get_style().item_spacing
    item_spacing_x = item_spacing.x

    input_text_right = button_label_width + (frame_padding_x * 2) + item_spacing_x
    imgui.set_next_item_width(-1 * input_text_right)
    left = input_text_multilingual(label, value, input_flags, input_size, input_hint)

    imgui.same_line()
    right = imgui.button(button_label)

    return left, right
