# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class ButtonFlags(IntFlag):
    mouse_button_left = imgui.ButtonFlags_.mouse_button_left.value
    mouse_button_middle = imgui.ButtonFlags_.mouse_button_middle.value
    mouse_button_right = imgui.ButtonFlags_.mouse_button_right.value


MOUSE_BUTTON_LEFT: Final[int] = int(ButtonFlags.mouse_button_left)
MOUSE_BUTTON_MIDDLE: Final[int] = int(ButtonFlags.mouse_button_middle)
MOUSE_BUTTON_RIGHT: Final[int] = int(ButtonFlags.mouse_button_right)


def merge_button_flags(*flags: Union[ButtonFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))


ALL_BUTTON_FLAGS: Final[int] = merge_button_flags(
    ButtonFlags.mouse_button_left,
    ButtonFlags.mouse_button_middle,
    ButtonFlags.mouse_button_right,
)
