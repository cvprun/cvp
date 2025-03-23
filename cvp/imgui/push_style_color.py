# -*- coding: utf-8 -*-

from contextlib import contextmanager

from imgui_bundle import imgui

from cvp.imgui.flags.color_var import CHILD_BG


@contextmanager
def style_color_child_background(r: float, g: float, b: float, a=1.0):
    imgui.push_style_color(CHILD_BG, (r, g, b, a))
    try:
        yield
    finally:
        imgui.pop_style_color()
