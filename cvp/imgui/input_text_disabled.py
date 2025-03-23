# -*- coding: utf-8 -*-

from typing import Union

from imgui_bundle import imgui

from cvp.imgui.flags.input_text import READ_ONLY, InputTextFlags
from cvp.imgui.push_style_var import (
    DEFAULT_DISABLE_BACKGROUND_COLOR,
    DEFAULT_DISABLE_TEXT_COLOR,
    style_disable_input,
)


def input_text_disabled(
    label: str,
    value: str,
    flags: Union[InputTextFlags, int] = 0,
    *,
    text_color=DEFAULT_DISABLE_TEXT_COLOR,
    background_color=DEFAULT_DISABLE_BACKGROUND_COLOR,
) -> None:
    if isinstance(flags, InputTextFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    with style_disable_input(text_color, background_color):
        imgui.input_text(label, value, flags | READ_ONLY)
