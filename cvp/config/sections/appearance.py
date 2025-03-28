# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique

from cvp.types.colors import BLACK_RGBA, RGBA


@unique
class AppMode(StrEnum):
    dashboard = auto()
    flow = auto()
    preference = auto()


@dataclass
class AppearanceConfig:
    theme: str = field(default_factory=str)
    mode: AppMode = field(default_factory=lambda: AppMode.dashboard)
    clear_color: RGBA = BLACK_RGBA
