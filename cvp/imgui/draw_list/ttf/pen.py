# -*- coding: utf-8 -*-

from typing import Optional, Union

from fontTools.pens.basePen import BasePen
from imgui_bundle import imgui

from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.draw_list.types import DrawList
from cvp.types.colors import RGB, RGBA
from cvp.types.override import override
from cvp.types.shapes import Point


class NoMoveToError(ValueError):
    def __init__(self):
        super().__init__("The path must start with a moveTo function")


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
        first_point: Optional[Point] = None,
    ):
        super().__init__(glyph_set)

        self.draw_list = draw_list if draw_list else get_window_draw_list()
        self.scale = scale
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.color = color if isinstance(color, int) else imgui.get_color_u32(color)
        self.thickness = thickness
        self.first_point = first_point

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

    @override
    def _moveTo(self, pt):
        self.first_point = self.calc_point(pt)
        self.draw_list.path_clear()
        self.draw_list.path_line_to(self.first_point)

    @override
    def _lineTo(self, pt):
        if self.first_point is None:
            raise NoMoveToError()

        self.draw_list.path_line_to(self.calc_point(pt))

    @override
    def _curveToOne(self, pt1, pt2, pt3):
        if self.first_point is None:
            raise NoMoveToError()

        self.draw_list.path_bezier_cubic_curve_to(
            self.calc_point(pt1),
            self.calc_point(pt2),
            self.calc_point(pt3),
        )

    @override
    def _qCurveToOne(self, pt1, pt2):
        if self.first_point is None:
            raise NoMoveToError()

        self.draw_list.path_bezier_quadratic_curve_to(
            self.calc_point(pt1),
            self.calc_point(pt2),
        )

    @override
    def _closePath(self):
        if self.first_point is None:
            raise NoMoveToError()

        self.draw_list.path_line_to(self.first_point)
        self.draw_list.path_stroke(self.color, 0, self.thickness)

        self.draw_list.path_clear()
        self.first_point = None

    @override
    def _endPath(self):
        if self.first_point is None:
            raise NoMoveToError()

        self.draw_list.path_clear()
        self.first_point = None
