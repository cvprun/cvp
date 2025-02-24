# -*- coding: utf-8 -*-

from abc import ABC
from typing import Sequence

from pygame import draw as pg_draw
from pygame.typing import RectLike

from cvp.pygame.surface._property import SurfacePropertyInterface
from cvp.pygame.types import ColorValue, Coordinate, SequenceProtocol


class Drawable(SurfacePropertyInterface, ABC):
    def draw_rect(
        self,
        color: ColorValue,
        rect: RectLike,
        width=0,
        border_radius=-1,
        border_top_left_radius=-1,
        border_top_right_radius=-1,
        border_bottom_left_radius=-1,
        border_bottom_right_radius=-1,
    ):
        return pg_draw.rect(
            self.surface,
            color,
            rect,
            width,
            border_radius,
            border_top_left_radius,
            border_top_right_radius,
            border_bottom_left_radius,
            border_bottom_right_radius,
        )

    def draw_polygon(self, color: ColorValue, points: Sequence[Coordinate], width=0):
        assert isinstance(points, SequenceProtocol)
        return pg_draw.polygon(self.surface, color, points, width)

    def draw_circle(
        self,
        color: ColorValue,
        center: Coordinate,
        radius: float,
        width=0,
        draw_top_right=False,
        draw_top_left=False,
        draw_bottom_left=False,
        draw_bottom_right=False,
    ):
        return pg_draw.circle(
            self.surface,
            color,
            center,
            radius,
            width,
            draw_top_right,
            draw_top_left,
            draw_bottom_left,
            draw_bottom_right,
        )

    def draw_ellipse(self, color: ColorValue, rect: RectLike, width=0):
        return pg_draw.ellipse(self.surface, color, rect, width)

    def draw_arc(
        self,
        color: ColorValue,
        rect: RectLike,
        start_angle: float,
        stop_angle: float,
        width=1,
    ):
        return pg_draw.arc(self.surface, color, rect, start_angle, stop_angle, width)

    def draw_line(
        self,
        color: ColorValue,
        start_pos: Coordinate,
        end_pos: Coordinate,
        width=1,
    ):
        return pg_draw.line(self.surface, color, start_pos, end_pos, width)

    def draw_lines(
        self,
        color: ColorValue,
        closed: bool,
        points: Sequence[Coordinate],
        width=1,
    ):
        assert isinstance(points, SequenceProtocol)
        return pg_draw.lines(self.surface, color, closed, points, width)

    def draw_aaline(
        self,
        color: ColorValue,
        start_pos: Coordinate,
        end_pos: Coordinate,
    ):
        return pg_draw.aaline(self.surface, color, start_pos, end_pos)

    def draw_aalines(
        self,
        color: ColorValue,
        closed: bool,
        points: Sequence[Coordinate],
    ):
        assert isinstance(points, SequenceProtocol)
        return pg_draw.aalines(self.surface, color, closed, points)
