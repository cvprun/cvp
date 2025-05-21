# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.colors import (
    BLACK_RGB,
    CYAN_RGBA,
    GREEN_RGBA,
    LIGHT_GRAY_RGBA,
    RED_RGBA,
    RGBA,
    WHITE_RGBA,
)
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

    background_color: RGBA = *BLACK_RGB, 0.6
    offset_color: RGBA = WHITE_RGBA
    red_color: RGBA = RED_RGBA
    green_color: RGBA = GREEN_RGBA
    blue_color: RGBA = CYAN_RGBA
    alpha_color: RGBA = LIGHT_GRAY_RGBA
