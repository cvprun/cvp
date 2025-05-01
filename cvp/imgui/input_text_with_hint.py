# -*- coding: utf-8 -*-

from typing import Union

from imgui_bundle import imgui

from cvp.imgui.flags.input_text import InputTextFlags
from cvp.imgui.input_text import InputTextResult


def input_text_with_hint(
    label: str,
    hint: str,
    value: str,
    flags: Union[InputTextFlags, int] = 0,
):
    if isinstance(flags, InputTextFlags):
        flags = int(flags)
    assert isinstance(flags, int)
    result = imgui.input_text_with_hint(label, hint, value, flags)
    return InputTextResult.from_raw(result)
