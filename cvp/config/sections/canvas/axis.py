# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.colors import RGBA
from cvp.variables import CANVAS_AXIS_COLOR, CANVAS_AXIS_THICKNESS, CANVAS_AXIS_VISIBLE


@dataclass
class Axis:
    visible: bool = CANVAS_AXIS_VISIBLE
    thickness: float = CANVAS_AXIS_THICKNESS
    color: RGBA = CANVAS_AXIS_COLOR
