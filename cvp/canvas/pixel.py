# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.colors import BLUE_RGBA, GREEN_RGBA, RED_RGBA, RGBA
from cvp.variables import (
    CANVAS_PIXEL_COLOR,
    CANVAS_PIXEL_THICKNESS,
    CANVAS_PIXEL_VISIBLE,
    CANVAS_PIXEL_ZOOM_THRESHOLD,
)


@dataclass
class Pixel:
    visible: bool = CANVAS_PIXEL_VISIBLE
    thickness: float = CANVAS_PIXEL_THICKNESS
    color: RGBA = CANVAS_PIXEL_COLOR
    zoom_threshold: float = CANVAS_PIXEL_ZOOM_THRESHOLD

    red_color: RGBA = RED_RGBA
    green_color: RGBA = GREEN_RGBA
    blue_color: RGBA = BLUE_RGBA
