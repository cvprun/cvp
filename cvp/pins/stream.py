# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class Stream(StrEnum):
    input = auto()
    output = auto()
