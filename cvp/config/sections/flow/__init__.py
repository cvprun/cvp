# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, NamedTuple, Optional

from cvp.config.sections.canvas.anchors import Anchors
from cvp.config.sections.canvas.axis import Axis
from cvp.config.sections.canvas.grid import Grid
from cvp.config.sections.canvas.roi import Roi
from cvp.config.sections.flow.logs import Logs
from cvp.config.sections.flow.nodes import Nodes
from cvp.config.sections.flow.pins import Pins
from cvp.config.sections.flow.wires import Wires
from cvp.itertools.find_index import find_index
from cvp.types.colors import RGBA
from cvp.variables import (
    FLOW_BACKGROUND_COLOR,
    FLOW_MAX_HISTORY,
    FLOW_PASTE_MARGIN,
    NOT_FOUND_INDEX,
)


class RecentItem(NamedTuple):
    path: str
    accessed_at: datetime

    @property
    def name(self):
        return os.path.basename(self.path)


@dataclass
class FlowConfig:
    recent: List[RecentItem] = field(default_factory=list)

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

    @staticmethod
    def _same_path(path1: str, path2: str) -> bool:
        return Path(path1).resolve() == Path(path2).resolve()

    def find_recent_index(self, path: str) -> int:
        return find_index(self.recent, key=lambda x: self._same_path(str(x), path))

    def add_recent(self, path: str, accessed_at: Optional[datetime] = None) -> None:
        if accessed_at is None:
            accessed_at = datetime.now().astimezone()
        assert isinstance(accessed_at, datetime)

        index = self.find_recent_index(path)
        if index != NOT_FOUND_INDEX:
            assert 0 <= index < len(self.recent)
            self.recent.pop(index)
        self.recent.append(RecentItem(path, accessed_at))
