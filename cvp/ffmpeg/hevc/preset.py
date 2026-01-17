# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Final


@unique
class Preset(StrEnum):
    """
    HEVC/H.265 encoding preset

    References:
        https://trac.ffmpeg.org/wiki/Encode/H.265
    """

    ultrafast = auto()
    superfast = auto()
    veryfast = auto()
    faster = auto()
    fast = auto()
    medium = auto()  # default preset
    slow = auto()
    slower = auto()
    veryslow = auto()
    placebo = auto()


DEFAULT_PRESET: Final[Preset] = Preset.medium
