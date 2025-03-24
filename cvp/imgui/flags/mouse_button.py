# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final

from imgui_bundle import imgui


@unique
class MouseButton(IntEnum):
    left = imgui.MouseButton_.left.value
    right = imgui.MouseButton_.right.value
    middle = imgui.MouseButton_.middle.value


MOUSE_LEFT: Final[int] = int(MouseButton.left)
MOUSE_RIGHT: Final[int] = int(MouseButton.right)
MOUSE_MIDDLE: Final[int] = int(MouseButton.middle)
