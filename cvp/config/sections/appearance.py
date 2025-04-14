# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.types.colors import (
    BLACK_RGBA,
    BLUE_RGBA,
    GREEN_RGBA,
    RED_RGBA,
    RGBA,
    WHITE_RGBA,
    YELLOW_RGBA,
)


@dataclass
class AppearanceConfig:
    theme: str = field(default_factory=str)
    mode: str = field(default_factory=str)

    clear_color: RGBA = BLACK_RGBA
    detail_color: RGBA = BLUE_RGBA
    success_color: RGBA = GREEN_RGBA
    normal_color: RGBA = WHITE_RGBA
    warning_color: RGBA = YELLOW_RGBA
    error_color: RGBA = RED_RGBA
