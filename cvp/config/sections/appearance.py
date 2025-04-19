# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Type

from cvp.types.colors import (
    BLACK_RGBA,
    BLUE_RGBA,
    GREEN_RGBA,
    RED_RGBA,
    RGBA,
    WHITE_RGBA,
    YELLOW_RGBA,
)
from cvp.variables import MODULE_PATH_SEPARATOR


@dataclass
class AppearanceConfig:
    theme: str = field(default_factory=str)
    mode: str = field(default_factory=str)
    selected_submenus: Dict[str, str] = field(default_factory=dict)

    clear_color: RGBA = BLACK_RGBA
    detail_color: RGBA = BLUE_RGBA

    success_color: RGBA = GREEN_RGBA
    normal_color: RGBA = WHITE_RGBA
    warning_color: RGBA = YELLOW_RGBA
    error_color: RGBA = RED_RGBA

    typename_color: RGBA = 1.0, 0.647, 0.0, 1.0

    @staticmethod
    def generate_selected_submenu_key(
        cls: Type,
        *,
        suffix: Optional[Any] = None,
        separator=MODULE_PATH_SEPARATOR,
    ) -> str:
        prefix = cls.__module__ + separator + cls.__name__
        return prefix + separator + str(suffix) if suffix is not None else prefix

    def get_selected_submenu(self, cls: Type, *, suffix: Optional[Any] = None) -> str:
        submenu_key = self.generate_selected_submenu_key(cls, suffix=suffix)
        return self.selected_submenus.get(submenu_key, str())

    def set_selected_submenu(
        self,
        cls: Type,
        value: str,
        *,
        suffix: Optional[Any] = None,
    ) -> None:
        submenu_key = self.generate_selected_submenu_key(cls, suffix=suffix)
        self.selected_submenus[submenu_key] = value
