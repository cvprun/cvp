# -*- coding: utf-8 -*-

from typing import Final

from cvp.imgui.draw_list.types import DrawList
from cvp.maths.geometry.dotted_line import create_dotted_line

DEFAULT_DOT_LENGTH: Final[float] = 5.0
DEFAULT_SPACE_LENGTH: Final[float] = 5.0


def draw_dotted_line(
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
    lines = create_dotted_line(x1, y1, x2, y2, dot_length, space_length)
    for start, end in lines:
        sx, sy = start
        ex, ey = end
        draw_list.add_line((sx, sy), (ex, ey), color, thickness)
