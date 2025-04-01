# -*- coding: utf-8 -*-

from contextlib import contextmanager

from imgui_bundle import imgui

from cvp.imgui.flags import color_var
from cvp.imgui.flags.color_var import CHILD_BG


@contextmanager
def style_color_child_background_context(r: float, g: float, b: float, a=1.0):
    imgui.push_style_color(CHILD_BG, (r, g, b, a))
    try:
        yield
    finally:
        imgui.pop_style_color()


@contextmanager
def style_disable_input_context(cancel=False):
    if not cancel:
        text_disabled_color = imgui.get_style_color_vec4(color_var.TEXT_DISABLED)
        imgui.push_style_color(color_var.TEXT, text_disabled_color)

        child_bg_color = imgui.get_style_color_vec4(color_var.CHILD_BG)
        imgui.push_style_color(color_var.FRAME_BG, child_bg_color)

    try:
        yield
    finally:
        if not cancel:
            imgui.pop_style_color(2)
