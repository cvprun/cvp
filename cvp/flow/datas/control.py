# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.variables import (
    BEZIER_CURVE_TESSELLATION_TOLERANCE,
    FLOW_ANCHOR_HOVERING_TOLERANCE,
    FLOW_ARCS_HOVERING_TOLERANCE,
)


@dataclass
class Control:
    pan_x: float = 0.0
    pan_y: float = 0.0
    zoom: float = 1.0

    bezier_curve_tessellation_tolerance: float = BEZIER_CURVE_TESSELLATION_TOLERANCE
    arc_hovering_tolerance: float = FLOW_ARCS_HOVERING_TOLERANCE
    anchor_hovering_tolerance: float = FLOW_ANCHOR_HOVERING_TOLERANCE
