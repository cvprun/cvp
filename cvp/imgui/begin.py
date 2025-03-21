# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def begin(label: str, closable=False, flags=0):
    return imgui.begin(label, closable, flags)


def end() -> None:
    imgui.end()
