# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Tuple

from cvp.logging.logging import DEBUG, ERROR, INFO, NOTSET, WARNING
from cvp.palette.basic import LIME, RED, WHITE, YELLOW
from cvp.types.colors import RGB


@dataclass
class ToastConfig:
    pivot_x: float = 0.5
    pivot_y: float = 1.0
    anchor_x: float = 0.5
    anchor_y: float = 1.0
    margin_x: float = 12.0
    margin_y: float = 12.0
    padding_x: float = 8.0
    padding_y: float = 8.0

    rounding: float = 15.0

    fadein: float = 0.5
    fadeout: float = 0.5
    waiting: float = 2.0

    background_color: RGB = 0.5, 0.5, 0.5
    success_color: RGB = LIME
    normal_color: RGB = WHITE
    warning_color: RGB = YELLOW
    error_color: RGB = RED

    @property
    def pivot(self) -> Tuple[float, float]:
        return self.pivot_x, self.pivot_y

    @pivot.setter
    def pivot(self, value: Tuple[float, float]) -> None:
        self.pivot_x = value[0]
        self.pivot_y = value[1]

    @property
    def anchor(self) -> Tuple[float, float]:
        return self.anchor_x, self.anchor_y

    @anchor.setter
    def anchor(self, value: Tuple[float, float]) -> None:
        self.anchor_x = value[0]
        self.anchor_y = value[1]

    @property
    def margin(self) -> Tuple[float, float]:
        return self.margin_x, self.margin_y

    @margin.setter
    def margin(self, value: Tuple[float, float]) -> None:
        self.margin_x = value[0]
        self.margin_y = value[1]

    @property
    def padding(self) -> Tuple[float, float]:
        return self.padding_x, self.padding_y

    @padding.setter
    def padding(self, value: Tuple[float, float]) -> None:
        self.padding_x = value[0]
        self.padding_y = value[1]

    def get_level_color(self, level: int) -> RGB:
        if WARNING < level <= ERROR:
            return self.error_color
        elif INFO < level <= WARNING:
            return self.warning_color
        elif DEBUG < level <= INFO:
            return self.normal_color
        elif NOTSET < level <= DEBUG:
            return self.success_color
        else:
            raise ValueError(f"Invalid level {level}")
