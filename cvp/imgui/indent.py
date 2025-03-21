# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import Union

from imgui_bundle import imgui


@contextmanager
def indent(width: Union[int, float]):
    imgui.indent(width)
    try:
        yield
    finally:
        imgui.unindent(width)
