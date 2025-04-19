# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass
class MediaManagerConfig:
    selected: str = field(default_factory=str)
