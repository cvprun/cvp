# -*- coding: utf-8 -*-

from abc import ABC
from typing import Sequence

from pygame import gfxdraw as pg_gfx
from pygame.surface import Surface
from pygame.typing import RectLike

from cvp.pygame.surface._property import SurfacePropertyInterface
from cvp.pygame.types import ColorValue, SequenceProtocol


class GfxDrawable(SurfacePropertyInterface, ABC):
    def gfx_pixel(self, x: int, y: int, color: ColorValue):
        return pg_gfx.pixel(self.surface, x, y, color)

    def gfx_hline(self, x1: int, x2: int, y: int, color: ColorValue):
        return pg_gfx.hline(self.surface, x1, x2, y, color)

    def gfx_vline(self, x: int, y1: int, y2: int, color: ColorValue):
        return pg_gfx.vline(self.surface, x, y1, y2, color)

    def gfx_line(self, x1: int, x2: int, y1: int, y2: int, color: ColorValue):
        return pg_gfx.line(self.surface, x1, y1, x2, y2, color)

    def gfx_rectangle(self, rect: RectLike, color: ColorValue):
        return pg_gfx.rectangle(self.surface, rect, color)

    def gfx_box(self, rect: RectLike, color: ColorValue):
        return pg_gfx.box(self.surface, rect, color)

    def gfx_circle(self, x: int, y: int, r: int, color: ColorValue):
        return pg_gfx.circle(self.surface, x, y, r, color)

    def gfx_aacircle(self, x: int, y: int, r: int, color: ColorValue):
        return pg_gfx.aacircle(self.surface, x, y, r, color)

    def gfx_filled_circle(self, x: int, y: int, r: int, color: ColorValue):
        return pg_gfx.filled_circle(self.surface, x, y, r, color)

    def gfx_ellipse(self, x: int, y: int, rx: int, ry: int, color: ColorValue):
        return pg_gfx.ellipse(self.surface, x, y, rx, ry, color)

    def gfx_aaellipse(self, x: int, y: int, rx: int, ry: int, color: ColorValue):
        return pg_gfx.aaellipse(self.surface, x, y, rx, ry, color)

    def gfx_filled_ellipse(self, x: int, y: int, rx: int, ry: int, color: ColorValue):
        return pg_gfx.filled_ellipse(self.surface, x, y, rx, ry, color)

    def gfx_arc(
        self,
        x: int,
        y: int,
        r: int,
        start_angle: int,
        atp_angle: int,
        color: ColorValue,
    ):
        return pg_gfx.arc(self.surface, x, y, r, start_angle, atp_angle, color)

    def gfx_pie(
        self,
        x: int,
        y: int,
        r: int,
        start_angle: int,
        atp_angle: int,
        color: ColorValue,
    ):
        return pg_gfx.pie(self.surface, x, y, r, start_angle, atp_angle, color)

    def gfx_trigon(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        x3: int,
        y3: int,
        color: ColorValue,
    ):
        return pg_gfx.trigon(self.surface, x1, y1, x2, y2, x3, y3, color)

    def gfx_aatrigon(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        x3: int,
        y3: int,
        color: ColorValue,
    ):
        return pg_gfx.aatrigon(self.surface, x1, y1, x2, y2, x3, y3, color)

    def gfx_filled_trigon(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        x3: int,
        y3: int,
        color: ColorValue,
    ):
        return pg_gfx.filled_trigon(self.surface, x1, y1, x2, y2, x3, y3, color)

    def gfx_polygon(self, points: Sequence[Sequence[float]], color: ColorValue):
        assert isinstance(points, SequenceProtocol)
        return pg_gfx.polygon(self.surface, points, color)

    def gfx_aapolygon(self, points: Sequence[Sequence[float]], color: ColorValue):
        assert isinstance(points, SequenceProtocol)
        return pg_gfx.aapolygon(self.surface, points, color)

    def gfx_filled_polygon(self, points: Sequence[Sequence[float]], color: ColorValue):
        assert isinstance(points, SequenceProtocol)
        return pg_gfx.filled_polygon(self.surface, points, color)

    def gfx_textured_polygon(
        self,
        points: Sequence[Sequence[float]],
        texture: Surface,
        tx: int,
        ty: int,
    ):
        assert isinstance(points, SequenceProtocol)
        return pg_gfx.textured_polygon(self.surface, points, texture, tx, ty)

    def gfx_bezier(
        self,
        points: Sequence[Sequence[float]],
        steps: int,
        color: ColorValue,
    ):
        assert isinstance(points, SequenceProtocol)
        return pg_gfx.bezier(self.surface, points, steps, color)
