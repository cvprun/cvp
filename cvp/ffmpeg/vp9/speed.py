# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final


@unique
class Speed(IntEnum):
    """
    VP9 encoding speed (cpu-used parameter)

    Lower values mean slower encoding but better quality.
    Range is -8 to 8, but practical range is 0 to 4.

    References:
        https://trac.ffmpeg.org/wiki/Encode/VP9
    """

    slowest = 0
    slow = 1
    medium = 2
    fast = 3
    fastest = 4


SPEED_MIN: Final[Speed] = Speed.slowest
SPEED_MAX: Final[Speed] = Speed.fastest
SPEED_DEFAULT: Final[Speed] = Speed.medium
