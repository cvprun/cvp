# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, NamedTuple

from cvp.config.sections.bases.aui import AuiWindowConfig
from cvp.config.sections.canvas.anchors import Anchors
from cvp.config.sections.canvas.axis import Axis
from cvp.config.sections.canvas.grid import Grid
from cvp.config.sections.canvas.roi import Roi
from cvp.config.sections.flow.logs import Logs
from cvp.config.sections.flow.nodes import Nodes
from cvp.config.sections.flow.pins import Pins
from cvp.config.sections.flow.wires import Wires
from cvp.types.colors import RGBA
from cvp.variables import (
    FLOW_BACKGROUND_COLOR,
    FLOW_MAX_HISTORY,
    FLOW_PASTE_MARGIN,
    MIN_SIDEBAR_HEIGHT,
)


class RecentItem(NamedTuple):
    uuid: str
    name: str
    updated_at: datetime


@dataclass
class FlowAuiConfig(AuiWindowConfig):
    recent: List[RecentItem] = field(default_factory=list)

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
    wires: Wires = field(default_factory=Wires)
    anchors: Anchors = field(default_factory=Anchors)

    roi: Roi = field(default_factory=Roi)
