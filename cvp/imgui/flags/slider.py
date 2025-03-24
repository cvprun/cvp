# -*- coding: utf-8 -*-

from enum import IntFlag, unique
from functools import reduce
from typing import Final, Union

from imgui_bundle import imgui


@unique
class SliderFlags(IntFlag):
    none = imgui.SliderFlags_.none.value
    logarithmic = imgui.SliderFlags_.logarithmic.value
    no_round_to_format = imgui.SliderFlags_.no_round_to_format.value
    no_input = imgui.SliderFlags_.no_input.value
    wrap_around = imgui.SliderFlags_.wrap_around.value
    clamp_on_input = imgui.SliderFlags_.clamp_on_input.value
    clamp_zero_range = imgui.SliderFlags_.clamp_zero_range.value
    no_speed_tweaks = imgui.SliderFlags_.no_speed_tweaks.value
    always_clamp = imgui.SliderFlags_.always_clamp.value
    invalid_mask_ = imgui.SliderFlags_.invalid_mask_.value


NONE: Final[int] = int(SliderFlags.none)
LOGARITHMIC: Final[int] = int(SliderFlags.logarithmic)
NO_ROUND_TO_FORMAT: Final[int] = int(SliderFlags.no_round_to_format)
NO_INPUT: Final[int] = int(SliderFlags.no_input)
WRAP_AROUND: Final[int] = int(SliderFlags.wrap_around)
CLAMP_ON_INPUT: Final[int] = int(SliderFlags.clamp_on_input)
CLAMP_ZERO_RANGE: Final[int] = int(SliderFlags.clamp_zero_range)
NO_SPEED_TWEAKS: Final[int] = int(SliderFlags.no_speed_tweaks)
ALWAYS_CLAMP: Final[int] = int(SliderFlags.always_clamp)


def merge_slider_flags(*flags: Union[SliderFlags, int]) -> int:
    return int(reduce(lambda x, y: x | y, flags))
