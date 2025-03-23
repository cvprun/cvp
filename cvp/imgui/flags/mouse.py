# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final

from imgui_bundle import imgui


@unique
class MouseButtonIndex(IntEnum):
    LEFT = imgui.MouseButton_.left.value
    MIDDLE = imgui.MouseButton_.middle.value
    RIGHT = imgui.MouseButton_.right.value


MOUSE_LEFT: Final[int] = int(MouseButtonIndex.LEFT)
MOUSE_MIDDLE: Final[int] = int(MouseButtonIndex.MIDDLE)
MOUSE_RIGHT: Final[int] = int(MouseButtonIndex.RIGHT)
