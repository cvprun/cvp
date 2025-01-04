# -*- coding: utf-8 -*-

from typing import List

from cvp.types.shapes import Point
from cvp.variables import BEZIER_CURVE_TESSELLATION_TOLERANCE


def _bezier_cubic_casteljau_points(
    path: List[Point],
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    x3: float,
    y3: float,
    x4: float,
    y4: float,
    tess_tol: float,
    level: int,
) -> None:
    dx = x4 - x1
    dy = y4 - y1
    d2 = (x2 - x4) * dy - (y2 - y4) * dx
    d3 = (x3 - x4) * dy - (y3 - y4) * dx

    d2 = d2 if d2 >= 0 else -d2
    d3 = d3 if d3 >= 0 else -d3

    if (d2 + d3) * (d2 + d3) < tess_tol * (dx * dx + dy * dy):
        path.append((x4, y4))
    elif level < 10:
        x12 = (x1 + x2) * 0.5
        y12 = (y1 + y2) * 0.5

        x23 = (x2 + x3) * 0.5
        y23 = (y2 + y3) * 0.5

        x34 = (x3 + x4) * 0.5
        y34 = (y3 + y4) * 0.5

        x123 = (x12 + x23) * 0.5
        y123 = (y12 + y23) * 0.5

        x234 = (x23 + x34) * 0.5
        y234 = (y23 + y34) * 0.5

        x1234 = (x123 + x234) * 0.5
        y1234 = (y123 + y234) * 0.5

        next_level = level + 1
        _bezier_cubic_casteljau_points(
            path=path,
            x1=x1,
            y1=y1,
            x2=x12,
            y2=y12,
            x3=x123,
            y3=y123,
            x4=x1234,
            y4=y1234,
            tess_tol=tess_tol,
            level=next_level,
        )
        _bezier_cubic_casteljau_points(
            path=path,
            x1=x1234,
            y1=y1234,
            x2=x234,
            y2=y234,
            x3=x34,
            y3=y34,
            x4=x4,
            y4=y4,
            tess_tol=tess_tol,
            level=next_level,
        )


def bezier_cubic_casteljau_points(
    p1: Point,
    p2: Point,
    p3: Point,
    p4: Point,
    tess_tol=BEZIER_CURVE_TESSELLATION_TOLERANCE,
) -> List[Point]:
    result = [p1]
    _bezier_cubic_casteljau_points(
        path=result,
        x1=p1[0],
        y1=p1[1],
        x2=p2[0],
        y2=p2[1],
        x3=p3[0],
        y3=p3[1],
        x4=p4[0],
        y4=p4[1],
        tess_tol=tess_tol,
        level=0,
    )
    return result
