# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.colors import RGBA
from cvp.variables import (
    FLOW_WIRE_HOVERING_COLOR,
    FLOW_WIRE_HOVERING_THICKNESS,
    FLOW_WIRE_NORMAL_COLOR,
    FLOW_WIRE_NORMAL_THICKNESS,
    FLOW_WIRE_SELECTED_COLOR,
    FLOW_WIRE_SELECTED_THICKNESS,
)


@dataclass
class Wires:
    selected_color: RGBA = FLOW_WIRE_SELECTED_COLOR
    hovering_color: RGBA = FLOW_WIRE_HOVERING_COLOR
    normal_color: RGBA = FLOW_WIRE_NORMAL_COLOR

    selected_thickness: float = FLOW_WIRE_SELECTED_THICKNESS
    hovering_thickness: float = FLOW_WIRE_HOVERING_THICKNESS
    normal_thickness: float = FLOW_WIRE_NORMAL_THICKNESS
