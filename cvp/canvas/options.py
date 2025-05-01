# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.variables import (
    BEZIER_CURVE_TESSELLATION_TOLERANCE,
    CANVAS_ANCHOR_HOVERING_TOLERANCE,
    CANVAS_LINE_HOVERING_TOLERANCE,
)


@dataclass
class DrawingOptions:
    bezier_curve_tessellation_tolerance: float = BEZIER_CURVE_TESSELLATION_TOLERANCE
    line_hovering_tolerance: float = CANVAS_LINE_HOVERING_TOLERANCE
    anchor_hovering_tolerance: float = CANVAS_ANCHOR_HOVERING_TOLERANCE
