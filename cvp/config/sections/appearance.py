# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique

from cvp.types.colors import (
    BLACK_RGBA,
    GREEN_RGBA,
    RED_RGBA,
    RGBA,
    WHITE_RGBA,
    YELLOW_RGBA,
)


@unique
class AppMode(StrEnum):
    dashboard = auto()
    chat = auto()
    flow = auto()
    preference = auto()


@dataclass
class AppearanceConfig:
    theme: str = field(default_factory=str)
    mode: AppMode = field(default_factory=lambda: AppMode.dashboard)
    clear_color: RGBA = BLACK_RGBA
    success_color: RGBA = GREEN_RGBA
    normal_color: RGBA = WHITE_RGBA
    warning_color: RGBA = YELLOW_RGBA
    error_color: RGBA = RED_RGBA
