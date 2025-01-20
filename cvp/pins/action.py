# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class Action(StrEnum):
    data = auto()
    flow = auto()
