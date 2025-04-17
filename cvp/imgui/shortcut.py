# -*- coding: utf-8 -*-

from typing import Union

from imgui_bundle import imgui

from cvp.imgui.flags.input_ import InputFlags
from cvp.imgui.flags.key import KeyFlags


def shortcut(keys: Union[KeyFlags, int], flags: Union[InputFlags, int] = 0):
    if isinstance(keys, KeyFlags):
        keys = int(keys)
    assert isinstance(keys, int)

    if isinstance(flags, InputFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    return imgui.shortcut(keys, flags)
