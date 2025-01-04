# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.colors import RGBA
from cvp.variables import (
    FLOW_ANCHOR_DRAWING_RADIUS,
    FLOW_ANCHOR_HOVERING_COLOR,
    FLOW_ANCHOR_NORMAL_COLOR,
    FLOW_ANCHOR_SELECTED_COLOR,
)


@dataclass
class Anchors:
    selected_color: RGBA = FLOW_ANCHOR_SELECTED_COLOR
    hovering_color: RGBA = FLOW_ANCHOR_HOVERING_COLOR
    normal_color: RGBA = FLOW_ANCHOR_NORMAL_COLOR
    radius: float = FLOW_ANCHOR_DRAWING_RADIUS
