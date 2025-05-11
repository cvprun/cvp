# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class DockPosition(StrEnum):
    left_top = auto()
    left_bottom = auto()

    center_top = auto()
    center_bottom = auto()

    right_top = auto()
    right_bottom = auto()
