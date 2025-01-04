# -*- coding: utf-8 -*-

from typing import List

from cvp.types.shapes import Point
from cvp.variables import BEZIER_CURVE_TESSELLATION_TOLERANCE


def _bezier_quadratic_casteljau_points(
    path: List[Point],
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    x3: float,
    y3: float,
    tess_tol: float,
    level: int,
) -> None:
    dx = x3 - x1
    dy = y3 - y1
    det = (x2 - x3) * dy - (y2 - y3) * dx

    if det * det * 4.0 < tess_tol * (dx * dx + dy * dy):
        path.append((x3, y3))
    elif level < 10:
        x12 = (x1 + x2) * 0.5
        y12 = (y1 + y2) * 0.5

        x23 = (x2 + x3) * 0.5
        y23 = (y2 + y3) * 0.5

        x123 = (x12 + x23) * 0.5
        y123 = (y12 + y23) * 0.5

        next_level = level + 1
        _bezier_quadratic_casteljau_points(
            path=path,
            x1=x1,
            y1=y1,
            x2=x12,
            y2=y12,
            x3=x123,
            y3=y123,
            tess_tol=tess_tol,
            level=next_level,
        )
        _bezier_quadratic_casteljau_points(
            path=path,
            x1=x123,
            y1=y123,
            x2=x23,
            y2=y23,
            x3=x3,
            y3=y3,
            tess_tol=tess_tol,
            level=next_level,
        )


def bezier_quadratic_casteljau_points(
    p1: Point,
    p2: Point,
    p3: Point,
    tess_tol=BEZIER_CURVE_TESSELLATION_TOLERANCE,
) -> List[Point]:
    result = [p1]
    _bezier_quadratic_casteljau_points(
        path=result,
        x1=p1[0],
        y1=p1[1],
        x2=p2[0],
        y2=p2[1],
        x3=p3[0],
        y3=p3[1],
        tess_tol=tess_tol,
        level=0,
    )
    return result
