# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.imgui.draw_list.types import DrawList
from cvp.types.shapes import Rect


def draw_centered_text(
    draw_list: DrawList,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: int,
    text: str,
) -> Rect:
    w = x2 - x1
    h = y2 - y1
    text_size = imgui.calc_text_size(text)
    tw, th = text_size.x, text_size.y
    x = x1 + (w - tw) / 2.0
    y = y1 + (h - th) / 2.0
    draw_list.add_text((x, y), color, text)
    return x, y, x + tw, y + th
