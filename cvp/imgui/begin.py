# -*- coding: utf-8 -*-

from typing import Union

from imgui_bundle import imgui

from cvp.imgui.flags.window import WindowFlags


def begin(label: str, closable=False, flags: Union[WindowFlags, int] = 0):
    return imgui.begin(label, closable, flags)


def end() -> None:
    imgui.end()
