# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.imgui.push_style_var import (
    DEFAULT_DISABLE_BACKGROUND_COLOR,
    DEFAULT_DISABLE_TEXT_COLOR,
    style_disable_input,
)

FORCE_READ_ONLY: Final[int] = imgui.INPUT_TEXT_READ_ONLY


def input_text_disabled(
    label: str,
    value: str,
    buffer_length=-1,
    flags=0,
    *,
    text_color=DEFAULT_DISABLE_TEXT_COLOR,
    background_color=DEFAULT_DISABLE_BACKGROUND_COLOR,
) -> None:
    with style_disable_input(text_color, background_color):
        imgui.input_text(label, value, buffer_length, flags | FORCE_READ_ONLY)
