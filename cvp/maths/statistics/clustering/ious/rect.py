# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Jaccard_index

from cvp.types.shapes import Rect


def calculate_iou(roi1: Rect, roi2: Rect) -> float:
    """
    Intersection over Union
    """

    lx1, ly1, lx2, ly2 = roi1
    rx1, ry1, rx2, ry2 = roi2

    # Calculate the coordinates of the intersection rectangle
    left = max(lx1, rx1)
    top = max(ly1, ry1)
    right = min(lx2, rx2)
    bottom = min(ly2, ry2)

    # If the rectangles do not intersect, return 0
    if right <= left or bottom <= top:
        return 0.0

    # Calculate the area of intersection
    intersection_area = (right - left) * (bottom - top)

    # Calculate the area of each rectangle
    area1 = (lx2 - lx1) * (ly2 - ly1)
    area2 = (rx2 - rx1) * (ry2 - ry1)

    # Calculate the union area
    union_area = area1 + area2 - intersection_area

    # Calculate IoU
    return intersection_area / union_area
