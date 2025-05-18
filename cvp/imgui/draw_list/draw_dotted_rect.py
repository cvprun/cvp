# -*- coding: utf-8 -*-

from cvp.imgui.draw_list.draw_dotted_line import (
    DEFAULT_DOT_LENGTH,
    DEFAULT_SPACE_LENGTH,
    draw_dotted_line,
)
from cvp.imgui.draw_list.types import DrawList


def draw_dotted_rect(
    draw_list: DrawList,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: int,
    thickness=1.0,
    dot_length=DEFAULT_DOT_LENGTH,
    space_length=DEFAULT_SPACE_LENGTH,
) -> None:
    line1 = x1, y1, x2, y1
    line2 = x2, y1, x2, y2
    line3 = x2, y2, x1, y2
    line4 = x1, y2, x1, y1
    draw_dotted_line(draw_list, *line1, color, thickness, dot_length, space_length)
    draw_dotted_line(draw_list, *line2, color, thickness, dot_length, space_length)
    draw_dotted_line(draw_list, *line3, color, thickness, dot_length, space_length)
    draw_dotted_line(draw_list, *line4, color, thickness, dot_length, space_length)
