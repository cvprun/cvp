# -*- coding: utf-8 -*-

from cvp.maths.geometry.bbox.normalize import normalize_bbox
from cvp.types.shapes import Rect


def calculate_bbox_intersection_area(roi1: Rect, roi2: Rect) -> float:
    lx1, ly1, lx2, ly2 = normalize_bbox(roi1)
    rx1, ry1, rx2, ry2 = normalize_bbox(roi2)

    # Calculate the coordinates of the intersection rectangle
    left = max(lx1, rx1)
    top = max(ly1, ry1)
    right = min(lx2, rx2)
    bottom = min(ly2, ry2)

    # If the rectangles do not intersect, return 0
    if left >= right or top >= bottom:
        return 0.0

    assert left < right
    assert top < bottom

    # Calculate the area of intersection
    intersection_area = (right - left) * (bottom - top)

    assert 0.0 < intersection_area
    return intersection_area


def is_bbox_area_overlapping(roi1: Rect, roi2: Rect) -> bool:
    """
    Returns True only for actual overlaps with positive area.

    - Edge/point contact: False
    - Area overlap: True
    """
    return 0.0 < calculate_bbox_intersection_area(roi1, roi2)


def is_bbox_boundary_contact(lh: Rect, rh: Rect) -> bool:
    """
    Returns True for any intersection including boundary contact.

    - Edge/point contact: True
    - Area overlap: True
    """
    lx1, ly1, lx2, ly2 = normalize_bbox(lh)
    rx1, ry1, rx2, ry2 = normalize_bbox(rh)
    return not (lx2 < rx1 or rx2 < lx1 or ly2 < ry1 or ry2 < ly1)
