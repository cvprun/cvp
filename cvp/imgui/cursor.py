# -*- coding: utf-8 -*-

from contextlib import contextmanager

from imgui_bundle import imgui


@contextmanager
def cursor_pos_x(y: float):
    original_x = imgui.get_cursor_pos_x()
    assert isinstance(original_x, float)

    try:
        imgui.set_cursor_pos_x(y)
        yield
    finally:
        imgui.set_cursor_pos_x(original_x)


@contextmanager
def cursor_pos_y(y: float):
    original_y = imgui.get_cursor_pos_y()
    assert isinstance(original_y, float)

    try:
        imgui.set_cursor_pos_y(y)
        yield
    finally:
        imgui.set_cursor_pos_y(original_y)
