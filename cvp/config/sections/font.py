# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Tuple

from cvp.config.sections.bases.manager import ManagerWindowConfig
from cvp.palette.basic import RED, WHITE
from cvp.types.colors import RGBA
from cvp.variables import (
    FONT_SCALE,
    FONT_SIZE,
    MAX_API_SELECT_WIDTH,
    MIN_API_SELECT_WIDTH,
)


@dataclass
class FontConfig:
    user_font: str = field(default_factory=str)
    scale: float = FONT_SCALE
    size: int = FONT_SIZE

    @property
    def size_pixels(self):
        return self.size * self.scale


@dataclass
class FontManagerConfig(ManagerWindowConfig):
    min_range_select_width: float = MIN_API_SELECT_WIDTH
    max_range_select_width: float = MAX_API_SELECT_WIDTH
    selected_block: Tuple[int, int] = field(default_factory=lambda: (0, 0))
    text_color: RGBA = field(default_factory=lambda: (*WHITE, 1.0))
    normal_stroke_color: RGBA = field(default_factory=lambda: (*WHITE, 0.3))
    error_stroke_color: RGBA = field(default_factory=lambda: (*RED, 0.3))
    rounding: float = 0.0
    rect_flags: int = 0
    thickness: float = 1.0
    padding: float = 4.0
