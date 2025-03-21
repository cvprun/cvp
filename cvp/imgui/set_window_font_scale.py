# -*- coding: utf-8 -*-

from contextlib import contextmanager

from imgui_bundle import imgui


@contextmanager
def window_font_scale(scale: float):
    original_scale = imgui.get_io().font_global_scale
    try:
        imgui.set_window_font_scale(scale)
        yield
    finally:
        imgui.set_window_font_scale(original_scale)
