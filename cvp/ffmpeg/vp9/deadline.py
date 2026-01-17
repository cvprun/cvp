# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Final


@unique
class Deadline(StrEnum):
    """
    VP9 encoding deadline

    Controls the encoding speed vs quality tradeoff.

    References:
        https://trac.ffmpeg.org/wiki/Encode/VP9
    """

    best = auto()
    """Slowest encoding, best quality"""

    good = auto()
    """Balanced encoding speed and quality"""

    realtime = auto()
    """Fastest encoding for real-time use"""


DEFAULT_DEADLINE: Final[Deadline] = Deadline.good
