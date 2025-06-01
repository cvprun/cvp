# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def radio_button(label: str, active: bool) -> bool:
    return imgui.radio_button(label, active)
