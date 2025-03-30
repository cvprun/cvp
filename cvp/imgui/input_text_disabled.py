# -*- coding: utf-8 -*-

from typing import Union

from imgui_bundle import imgui

from cvp.imgui.flags.input_text import READ_ONLY, InputTextFlags
from cvp.imgui.push_style_var import style_disable_input_context


def input_text_disabled(
    label: str,
    value: str,
    flags: Union[InputTextFlags, int] = 0,
) -> None:
    if isinstance(flags, InputTextFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    with style_disable_input_context():
        imgui.input_text(label, value, flags | READ_ONLY)
