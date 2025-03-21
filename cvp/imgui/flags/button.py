# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from typing import Final

from imgui_bundle import imgui


@unique
class ButtonFlags(IntFlag):
    MOUSE_BUTTON_LEFT = imgui.BUTTON_MOUSE_BUTTON_LEFT
    MOUSE_BUTTON_MIDDLE = imgui.BUTTON_MOUSE_BUTTON_MIDDLE
    MOUSE_BUTTON_RIGHT = imgui.BUTTON_MOUSE_BUTTON_RIGHT


LEFT_BUTTON_FLAGS: Final[ButtonFlags] = ButtonFlags.MOUSE_BUTTON_LEFT
MIDDLE_BUTTON_FLAGS: Final[ButtonFlags] = ButtonFlags.MOUSE_BUTTON_MIDDLE
RIGHT_BUTTON_FLAGS: Final[ButtonFlags] = ButtonFlags.MOUSE_BUTTON_RIGHT

ALL_BUTTON_FLAGS: Final[ButtonFlags] = (
    LEFT_BUTTON_FLAGS | MIDDLE_BUTTON_FLAGS | RIGHT_BUTTON_FLAGS
)
