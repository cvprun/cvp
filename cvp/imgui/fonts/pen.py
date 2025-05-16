# -*- coding: utf-8 -*-

from typing import Optional, Union

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


class ImguiPen(BasePen):
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
        *,
        first_point: Optional[Point] = None,
        last_point: Optional[Point] = None,
    ):
        super().__init__(glyph_set)

        self.draw_list = draw_list if draw_list else get_window_draw_list()
        self.scale = scale
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.color = color if isinstance(color, int) else imgui.get_color_u32(color)
        self.thickness = thickness
        self.tess_tol = tess_tol

        self._first_point = first_point
        self._last_point = last_point

    def calc_x(self, value: float) -> float:
        return +1 * value * self.scale + self.offset_x

    def calc_y(self, value: float) -> float:
        return -1 * value * self.scale + self.offset_x

    def calc_point(self, point: Point) -> Point:
        x = self.calc_x(point[0])
        y = self.calc_x(point[1])
        return x, y

    def set_rgba_color(self, color: RGBA) -> None:
        self.color = imgui.get_color_u32(color)

    def set_rgb_color(self, color: RGB, alpha=1.0) -> None:
        self.color = imgui.get_color_u32((*color, alpha))

    def set_u32_color(self, color: int) -> None:
        self.color = color

    @override
    def _moveTo(self, pt):
        self._first_point = self.calc_point(pt)
        self._last_point = self._first_point

    @override
    def _lineTo(self, pt):
        if self._last_point is None:
            raise ValueError("moveTo must be called before lineTo")

        new_point = self.calc_point(pt)
        self.draw_list.add_line(
            self._last_point,
            new_point,
            self.color,
            self.thickness,
        )
        self._last_point = new_point

    @override
    def _curveToOne(self, pt1, pt2, pt3):
        if self._last_point is None:
            raise ValueError("moveTo must be called before lineTo")

        p1 = self.calc_point(pt1)
        p2 = self.calc_point(pt2)
        p3 = self.calc_point(pt3)

        points = bezier_cubic_casteljau_points(
            self._last_point,
            p1,
            p2,
            p3,
            self.tess_tol,
        )
        self.draw_list.add_polyline(points, self.color, 0, self.thickness)
        self._last_point = p3

    @override
    def _closePath(self):
        if self._first_point is None or self._last_point is None:
            raise ValueError("moveTo must be called before lineTo")

        self.draw_list.add_line(
            self._last_point,
            self._first_point,
            self.color,
            self.thickness,
        )

    @override
    def _endPath(self):
        self._first_point = None
        self._last_point = None

    @override
    def _qCurveToOne(self, pt1, pt2):
        if self._last_point is None:
            raise ValueError("moveTo must be called before lineTo")

        p1 = self.calc_point(pt1)
        p2 = self.calc_point(pt2)
        points = bezier_quadratic_casteljau_points(
            self._last_point,
            p1,
            p2,
            self.tess_tol,
        )
        self.draw_list.add_polyline(points, self.color, 0, self.thickness)
        self._last_point = p2
