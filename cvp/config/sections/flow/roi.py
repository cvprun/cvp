# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.colors import RGBA
from cvp.variables import FLOW_ROI_COLOR, FLOW_ROI_ROUNDING, FLOW_ROI_THICKNESS


@dataclass
class Roi:
    color: RGBA = FLOW_ROI_COLOR
    rounding: float = FLOW_ROI_ROUNDING
    thickness: float = FLOW_ROI_THICKNESS
