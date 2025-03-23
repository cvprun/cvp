# -*- coding: utf-8 -*-

from imgui_bundle import imgui


def button(label: str, width=0.0, height=0.0, disabled=False) -> bool:
    if disabled:
        imgui.push_style_var(imgui.StyleVar_.alpha.value, imgui.get_style().alpha * 0.5)

    clicked = imgui.button(label, (width, height))

    if disabled:
        imgui.pop_style_var()
        return False
    else:
        return clicked
