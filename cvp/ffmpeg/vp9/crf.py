# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final


@unique
class Crf(IntEnum):
    """
    Constant Rate Factor for VP9

    The CRF scale is 0–63, where 0 is best quality, and 63 is worst.
    Recommended values are 15-35, with 31 being a good starting point.

    References:
        https://trac.ffmpeg.org/wiki/Encode/VP9
    """

    best_quality = 0
    high_quality = 15
    default = 31
    low_quality = 35
    worst_quality = 63
    sane_range_min = 15
    sane_range_max = 35


CRF_MIN: Final[Crf] = Crf.best_quality
CRF_MAX: Final[Crf] = Crf.worst_quality
CRF_DEFAULT: Final[Crf] = Crf.default
