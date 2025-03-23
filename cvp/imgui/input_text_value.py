# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE


def input_text_value(
    label: str,
    value: str,
    buffer_length=-1,
    flags=ENTER_RETURNS_TRUE,
) -> str:
    changed, value = imgui.input_text(label, value, buffer_length, flags)
    assert isinstance(changed, bool)
    assert isinstance(value, str)
    return value
