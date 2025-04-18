# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.palette.basic import GREEN, RED, YELLOW
from cvp.types.colors import RGBA
from cvp.variables import API_SELECT_WIDTH, MAX_API_SELECT_WIDTH, MIN_API_SELECT_WIDTH


@dataclass
class OnvifManagerConfig:
    preload: bool = False

    selected: str = field(default_factory=str)

    api_select_width: float = API_SELECT_WIDTH
    min_api_select_width: float = MIN_API_SELECT_WIDTH
    max_api_select_width: float = MAX_API_SELECT_WIDTH

    success_color: RGBA = field(default_factory=lambda: (*GREEN, 1.0))
    error_color: RGBA = field(default_factory=lambda: (*RED, 1.0))
    warning_color: RGBA = field(default_factory=lambda: (*YELLOW, 1.0))
    typename_color: RGBA = field(default_factory=lambda: (1.0, 0.647, 0.0, 1.0))
