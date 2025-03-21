# -*- coding: utf-8 -*-

from contextlib import contextmanager

from imgui_bundle import imgui


@contextmanager
def font_global_scale(scale: float):
    original_scale = imgui.get_io().font_global_scale
    try:
        imgui.get_io().font_global_scale = scale
        yield
    finally:
        imgui.get_io().font_global_scale = original_scale
