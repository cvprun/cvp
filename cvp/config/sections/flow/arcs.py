# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.colors import RGBA
from cvp.variables import (
    FLOW_ARC_HOVERING_COLOR,
    FLOW_ARC_HOVERING_THICKNESS,
    FLOW_ARC_NORMAL_COLOR,
    FLOW_ARC_NORMAL_THICKNESS,
    FLOW_ARC_SELECTED_COLOR,
    FLOW_ARC_SELECTED_THICKNESS,
)


@dataclass
class Arcs:
    selected_color: RGBA = FLOW_ARC_SELECTED_COLOR
    hovering_color: RGBA = FLOW_ARC_HOVERING_COLOR
    normal_color: RGBA = FLOW_ARC_NORMAL_COLOR

    selected_thickness: float = FLOW_ARC_SELECTED_THICKNESS
    hovering_thickness: float = FLOW_ARC_HOVERING_THICKNESS
    normal_thickness: float = FLOW_ARC_NORMAL_THICKNESS
