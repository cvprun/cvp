# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final


@unique
class Preset(IntEnum):
    """
    AV1 encoding preset for SVT-AV1

    Range is 0-13, where 0 is slowest/best quality and 13 is fastest.
    Preset 8-10 provides a good balance for most use cases.

    References:
        https://trac.ffmpeg.org/wiki/Encode/AV1
        https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/Docs/Ffmpeg.md
    """

    slowest = 0
    very_slow = 2
    slow = 4
    medium = 6
    fast = 8
    very_fast = 10
    fastest = 13


DEFAULT_PRESET: Final[Preset] = Preset.medium
