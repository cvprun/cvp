# -*- coding: utf-8 -*-

from typing import Iterable, List

from cvp.types.shapes import Point, Rect


def rescale_points(
    src_points: Iterable[Point],
    src_roi: Rect,
    dest_roi: Rect,
) -> List[Point]:
    src_x1, src_y1, src_x2, src_y2 = src_roi
    dest_x1, dest_y1, dest_x2, dest_y2 = dest_roi

    src_width = src_x2 - src_x1
    src_height = src_y2 - src_y1
    dest_width = dest_x2 - dest_x1
    dest_height = dest_y2 - dest_y1

    if 0 == src_width or 0 == src_height:
        raise ValueError("The src ROI must have a non-zero width or height")
    if 0 == dest_width or 0 == dest_height:
        raise ValueError("The dest ROI must have a non-zero width or height")

    scale_x = dest_width / src_width
    scale_y = dest_height / src_height

    result = list()
    for x, y in src_points:
        dest_x = dest_x1 + (x - src_x1) * scale_x
        dest_y = dest_y1 + (y - src_y1) * scale_y
        result.append((dest_x, dest_y))
    return result
