# -*- coding: utf-8 -*-

from enum import IntEnum, auto, unique


@unique
class FlowMode(IntEnum):
    normal = auto()
    node_moving = auto()
    pin_connecting = auto()
    anchor_moving = auto()
    roi_box = auto()
