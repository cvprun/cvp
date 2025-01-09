# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List

from cvp.config.sections.bases.window import WindowConfig
from cvp.config.sections.canvas.anchors import Anchors
from cvp.config.sections.canvas.axis import Axis
from cvp.config.sections.canvas.grid import Grid
from cvp.config.sections.canvas.roi import Roi


@dataclass
class CanvasWindowConfig(WindowConfig):
    history: List[str] = field(default_factory=list)
    files: List[str] = field(default_factory=list)

    grid_x: Grid = field(default_factory=Grid)
    grid_y: Grid = field(default_factory=Grid)

    axis_x: Axis = field(default_factory=Axis)
    axis_y: Axis = field(default_factory=Axis)

    anchors: Anchors = field(default_factory=Anchors)
    roi: Roi = field(default_factory=Roi)
