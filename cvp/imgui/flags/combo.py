# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class ComboFlags(IntFlag):
    none = imgui.ComboFlags_.none.value
    popup_align_left = imgui.ComboFlags_.popup_align_left.value
    height_small = imgui.ComboFlags_.height_small.value
    height_regular = imgui.ComboFlags_.height_regular.value
    height_large = imgui.ComboFlags_.height_large.value
    height_largest = imgui.ComboFlags_.height_largest.value
    no_arrow_button = imgui.ComboFlags_.no_arrow_button.value
    no_preview = imgui.ComboFlags_.no_preview.value
    width_fit_preview = imgui.ComboFlags_.width_fit_preview.value


NONE: Final[int] = int(ComboFlags.none)
POPUP_ALIGN_LEFT: Final[int] = int(ComboFlags.popup_align_left)
HEIGHT_SMALL: Final[int] = int(ComboFlags.height_small)
HEIGHT_REGULAR: Final[int] = int(ComboFlags.height_regular)
HEIGHT_LARGE: Final[int] = int(ComboFlags.height_large)
HEIGHT_LARGEST: Final[int] = int(ComboFlags.height_largest)
NO_ARROW_BUTTON: Final[int] = int(ComboFlags.no_arrow_button)
NO_PREVIEW: Final[int] = int(ComboFlags.no_preview)
WIDTH_FIT_PREVIEW: Final[int] = int(ComboFlags.width_fit_preview)


def merge_combo_flags(*flags: Union[ComboFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))
