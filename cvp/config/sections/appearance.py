# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from enum import StrEnum, auto, unique

from cvp.types.colors import BLACK_RGBA, RGBA
from cvp.variables import GUI_THEME


@unique
class AppMode(StrEnum):
    none = auto()
    preference = auto()


@dataclass
class AppearanceConfig:
    theme: str = GUI_THEME
    mode: AppMode = field(default_factory=lambda: AppMode.none)
    clear_color: RGBA = BLACK_RGBA
