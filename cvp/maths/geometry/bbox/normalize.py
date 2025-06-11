# -*- coding: utf-8 -*-

from cvp.types.shapes import Rect


def normalize_bbox(rect: Rect) -> Rect:
    x1, y1, x2, y2 = rect

    left = min(x1, x2)
    right = max(x1, x2)

    top = min(y1, y2)
    bottom = max(y1, y2)

    return left, top, right, bottom
