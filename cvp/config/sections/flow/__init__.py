# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.config.sections.bases.aui import AuiWindowConfig
from cvp.config.sections.canvas.anchors import Anchors
from cvp.config.sections.canvas.axis import Axis
from cvp.config.sections.canvas.grid import Grid
from cvp.config.sections.canvas.roi import Roi
from cvp.config.sections.flow.arcs import Arcs
from cvp.config.sections.flow.logs import Logs
from cvp.config.sections.flow.nodes import Nodes
from cvp.config.sections.flow.pins import Pins
from cvp.types.colors import RGBA
from cvp.variables import (
    FLOW_BACKGROUND_COLOR,
    FLOW_MAX_HISTORY,
    FLOW_PASTE_MARGIN,
    MIN_SIDEBAR_HEIGHT,
)


@dataclass
class FlowAuiConfig(AuiWindowConfig):
    split_tree: float = MIN_SIDEBAR_HEIGHT
    min_split_tree: float = MIN_SIDEBAR_HEIGHT

    background_color: RGBA = FLOW_BACKGROUND_COLOR
    max_history: int = FLOW_MAX_HISTORY
    paste_margin: float = FLOW_PASTE_MARGIN

    logs: Logs = field(default_factory=Logs)

    grid_x: Grid = field(default_factory=Grid)
    grid_y: Grid = field(default_factory=Grid)

    axis_x: Axis = field(default_factory=Axis)
    axis_y: Axis = field(default_factory=Axis)

    nodes: Nodes = field(default_factory=Nodes)
    pins: Pins = field(default_factory=Pins)
    arcs: Arcs = field(default_factory=Arcs)
    anchors: Anchors = field(default_factory=Anchors)

    roi: Roi = field(default_factory=Roi)
