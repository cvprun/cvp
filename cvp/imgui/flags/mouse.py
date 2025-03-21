# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final

from imgui_bundle import imgui


@unique
class MouseButtonIndex(IntEnum):
    LEFT = imgui.MOUSE_BUTTON_LEFT
    MIDDLE = imgui.MOUSE_BUTTON_MIDDLE
    RIGHT = imgui.MOUSE_BUTTON_RIGHT


MOUSE_LEFT: Final[MouseButtonIndex] = MouseButtonIndex.LEFT
MOUSE_MIDDLE: Final[MouseButtonIndex] = MouseButtonIndex.MIDDLE
MOUSE_RIGHT: Final[MouseButtonIndex] = MouseButtonIndex.RIGHT
