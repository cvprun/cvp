# -*- coding: utf-8 -*-

from cvp.types.shapes import Rect


def normalize_rectangle(rect: Rect) -> Rect:
    x1, y1, x2, y2 = rect
    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)
    return left, top, right, bottom


def is_rectangle_collision(lh: Rect, rh: Rect) -> bool:
    lx1, ly1, lx2, ly2 = normalize_rectangle(lh)
    rx1, ry1, rx2, ry2 = normalize_rectangle(rh)
    return not (lx2 < rx1 or rx2 < lx1 or ly2 < ry1 or ry2 < ly1)
