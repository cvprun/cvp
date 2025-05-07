# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class InputMethodMode(StrEnum):
    english = auto()
    hangul = auto()
