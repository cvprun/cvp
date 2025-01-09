# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.colors import RGBA
from cvp.variables import (
    CANVAS_ANCHOR_DRAWING_RADIUS,
    CANVAS_ANCHOR_HOVERING_COLOR,
    CANVAS_ANCHOR_NORMAL_COLOR,
    CANVAS_ANCHOR_SELECTED_COLOR,
)


@dataclass
class Anchors:
    selected_color: RGBA = CANVAS_ANCHOR_SELECTED_COLOR
    hovering_color: RGBA = CANVAS_ANCHOR_HOVERING_COLOR
    normal_color: RGBA = CANVAS_ANCHOR_NORMAL_COLOR
    radius: float = CANVAS_ANCHOR_DRAWING_RADIUS
