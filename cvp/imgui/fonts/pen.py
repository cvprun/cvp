# -*- coding: utf-8 -*-

from typing import List, Optional, Union

from fontTools.pens.basePen import BasePen
from imgui_bundle import imgui

from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.draw_list.types import DrawList
from cvp.maths.bezier.casteljau.cubic import bezier_cubic_casteljau_points
from cvp.maths.bezier.casteljau.quadratic import bezier_quadratic_casteljau_points
from cvp.types.colors import RGB, RGBA
from cvp.types.override import override
from cvp.types.shapes import Point
from cvp.variables import BEZIER_CURVE_TESSELLATION_TOLERANCE


class EmptyPathError(ValueError):
    def __init__(self):
        super().__init__("The path must start with a moveTo function")


class ImguiPen(BasePen):
    _path: List[Point]

    def __init__(
        self,
        glyph_set=None,
        draw_list: Optional[DrawList] = None,
        scale=1.0,
        offset_x=0.0,
        offset_y=0.0,
        color: Union[int, RGBA] = 0xFFFFFFFF,
        thickness=1.0,
        tess_tol=BEZIER_CURVE_TESSELLATION_TOLERANCE,
    ):
        super().__init__(glyph_set)

        self.draw_list = draw_list if draw_list else get_window_draw_list()
        self.scale = scale
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.color = color if isinstance(color, int) else imgui.get_color_u32(color)
        self.thickness = thickness
        self.tess_tol = tess_tol

        self._path = list()

    def calc_x(self, value: float) -> float:
        return self.offset_x + (value * self.scale)

    def calc_y(self, value: float) -> float:
        return self.offset_y - (value * self.scale)

    def calc_point(self, point: Point) -> Point:
        x = self.calc_x(point[0])
        y = self.calc_y(point[1])
        return x, y

    def set_rgba_color(self, color: RGBA) -> None:
        self.color = imgui.get_color_u32(color)

    def set_rgb_color(self, color: RGB, alpha=1.0) -> None:
        self.color = imgui.get_color_u32((*color, alpha))

    def set_u32_color(self, color: int) -> None:
        self.color = color

    @property
    def first_point(self):
        return self._path[0]

    @property
    def last_point(self):
        return self._path[-1]

    @override
    def _moveTo(self, pt):
        self._path = [self.calc_point(pt)]

    @override
    def _lineTo(self, pt):
        if not self._path:
            raise EmptyPathError()

        new_point = self.calc_point(pt)
        self.draw_list.add_line(
            self.last_point,
            new_point,
            self.color,
            self.thickness,
        )
        self._path.append(new_point)

    @override
    def _curveToOne(self, pt1, pt2, pt3):
        if not self._path:
            raise EmptyPathError()

        points = bezier_cubic_casteljau_points(
            self.last_point,
            self.calc_point(pt1),
            self.calc_point(pt2),
            self.calc_point(pt3),
            self.tess_tol,
        )

        prev_point = points[0]
        for next_point in points[1:]:
            self.draw_list.add_line(prev_point, next_point, self.color, self.thickness)
            self._path.append(next_point)
            prev_point = next_point

    @override
    def _closePath(self):
        if not self._path:
            raise EmptyPathError()

        new_point = self.first_point
        self.draw_list.add_line(
            self.last_point,
            new_point,
            self.color,
            self.thickness,
        )
        self._path.append(new_point)

    @override
    def _endPath(self):
        self._path.clear()

    @override
    def _qCurveToOne(self, pt1, pt2):
        if not self._path:
            raise EmptyPathError()

        points = bezier_quadratic_casteljau_points(
            self.last_point,
            self.calc_point(pt1),
            self.calc_point(pt2),
            self.tess_tol,
        )

        prev_point = points[0]
        for next_point in points[1:]:
            self.draw_list.add_line(prev_point, next_point, self.color, self.thickness)
            self._path.append(next_point)
            prev_point = next_point
