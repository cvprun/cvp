# -*- coding: utf-8 -*-

from typing import NamedTuple


class ControllableResult(NamedTuple):
    changed: bool
    pan_x: float = 0.0
    pan_y: float = 0.0
    zoom: float = 1.0

    def __bool__(self) -> bool:
        return self.changed

    @property
    def pan(self):
        return self.pan_x, self.pan_y
