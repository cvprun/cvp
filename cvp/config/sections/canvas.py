# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass
class CanvasConfig:
    selected_uuid: str = field(default_factory=str)
