# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import Union

from imgui_bundle import imgui


@contextmanager
def item_width_context(width: Union[int, float]):
    imgui.push_item_width(width)
    try:
        yield
    finally:
        imgui.pop_item_width()


@contextmanager
def align_right_side_context():
    imgui.push_item_width(-imgui.FLT_MIN)
    try:
        yield
    finally:
        imgui.pop_item_width()
