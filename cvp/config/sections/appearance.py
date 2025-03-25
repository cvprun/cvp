# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.types.colors import BLACK_RGBA, RGBA
from cvp.variables import GUI_THEME


@dataclass
class AppearanceConfig:
    theme: str = GUI_THEME
    clear_color: RGBA = BLACK_RGBA
