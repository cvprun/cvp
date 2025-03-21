# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

ENTER_RETURN: Final[int] = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE


def input_text_value(
    label: str,
    value: str,
    buffer_length=-1,
    flags=ENTER_RETURN,
) -> str:
    changed, value = imgui.input_text(label, value, buffer_length, flags)
    assert isinstance(changed, bool)
    assert isinstance(value, str)
    return value
