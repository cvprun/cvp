# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import IntEnum, unique

from cvp.types.colors import GREEN_RGBA, RED_RGBA, RGBA, YELLOW_RGBA


@unique
class Anchor(IntEnum):
    top_left = 0
    top_right = 1
    bottom_left = 2
    bottom_right = 3


@dataclass
class OverlayConfig:
    opened: bool = False
    anchor: Anchor = Anchor.top_left
    padding: float = 10.0
    alpha: float = 0.2

    fps_warning_threshold: float = 30.0
    fps_error_threshold: float = 8.0

    error_color: RGBA = RED_RGBA
    normal_color: RGBA = GREEN_RGBA
    warning_color: RGBA = YELLOW_RGBA

    @property
    def is_top_left(self):
        return self.anchor == Anchor.top_left

    @property
    def is_top_right(self):
        return self.anchor == Anchor.top_right

    @property
    def is_bottom_left(self):
        return self.anchor == Anchor.bottom_left

    @property
    def is_bottom_right(self):
        return self.anchor == Anchor.bottom_right

    def set_top_left(self) -> None:
        self.anchor = Anchor.top_left

    def set_top_right(self) -> None:
        self.anchor = Anchor.top_right

    def set_bottom_left(self) -> None:
        self.anchor = Anchor.bottom_left

    def set_bottom_right(self) -> None:
        self.anchor = Anchor.bottom_right

    @property
    def is_left_side(self):
        return self.anchor in (Anchor.top_left, Anchor.bottom_left)

    @property
    def is_right_side(self):
        return not self.is_left_side

    @property
    def is_top_side(self):
        return self.anchor in (Anchor.top_left, Anchor.top_right)

    @property
    def is_bottom_side(self):
        return not self.is_top_side

    def get_framerate_color(self, framerate: float) -> RGBA:
        if framerate >= self.fps_warning_threshold:
            return self.normal_color
        elif framerate >= self.fps_error_threshold:
            return self.warning_color
        else:
            return self.error_color
