# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.colors import RGBA
from cvp.variables import CANVAS_ROI_COLOR, CANVAS_ROI_ROUNDING, CANVAS_ROI_THICKNESS


@dataclass
class Roi:
    color: RGBA = CANVAS_ROI_COLOR
    rounding: float = CANVAS_ROI_ROUNDING
    thickness: float = CANVAS_ROI_THICKNESS
