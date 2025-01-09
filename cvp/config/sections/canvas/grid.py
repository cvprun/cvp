# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.colors import RGBA
from cvp.variables import (
    CANVAS_GRID_COLOR,
    CANVAS_GRID_STEP,
    CANVAS_GRID_THICKNESS,
    CANVAS_GRID_VISIBLE,
)


@dataclass
class Grid:
    visible: bool = CANVAS_GRID_VISIBLE
    step: float = CANVAS_GRID_STEP
    thickness: float = CANVAS_GRID_THICKNESS
    color: RGBA = CANVAS_GRID_COLOR
