# -*- coding: utf-8 -*-

from typing import List, Tuple, Union

from fontTools.pens.basePen import BasePen

from cvp.imgui.draw_list.types import DrawList
from cvp.maths.bezier.casteljau.quadratic import bezier_quadratic_casteljau_points
from cvp.types.override import override
from cvp.variables import BEZIER_CURVE_TESSELLATION_TOLERANCE


class ImguiPen(BasePen):
    path: List[Tuple[Union[float, int], Union[float, int]]]

    def __init__(
        self,
        glyph_set,
        draw_list: DrawList,
        scale=1.0,
        offset_x=0,
        offset_y=0,
        color=0xFFFFFFFF,
        thickness=1.0,
    ):
        super().__init__(glyph_set)
        self.draw_list = draw_list
        self.scale = scale
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.color = color
        self.current_point = None
        self.first_point = None
        self.path = list()
        self.thickness = thickness
        self.tess_tol = BEZIER_CURVE_TESSELLATION_TOLERANCE

    @override
    def _moveTo(self, pt):
        x = +1 * pt[0] * self.scale + self.offset_x
        y = -1 * pt[1] * self.scale + self.offset_y
        self.current_point = x, y
        self.first_point = self.current_point
        self.path = [self.current_point]

    @override
    def _lineTo(self, pt):
        x = +1 * pt[0] * self.scale + self.offset_x
        y = -1 * pt[1] * self.scale + self.offset_y
        new_point = x, y
        self.draw_list.add_line(
            self.current_point,
            new_point,
            self.color,
            self.thickness,
        )
        self.current_point = new_point
        self.path.append(self.current_point)

    @override
    def _curveToOne(self, pt1, pt2, pt3):
        points = bezier_quadratic_casteljau_points(pt1, pt2, pt3)
        self.draw_list.add_polyline(points, self.color, 0, self.thickness)
