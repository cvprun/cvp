# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final


@unique
class Crf(IntEnum):
    """
    Constant Rate Factor for HEVC/H.265

    The CRF scale is 0–51, where 0 is lossless, 28 is the default,
    and 51 is worst quality possible.

    References:
        https://trac.ffmpeg.org/wiki/Encode/H.265
    """

    lossless = 0
    visually_lossless = 18
    default = 28
    worst_quality_possible = 51
    sane_range_min = 18
    sane_range_max = 28


CRF_MIN: Final[Crf] = Crf.lossless
CRF_MAX: Final[Crf] = Crf.worst_quality_possible
CRF_DEFAULT: Final[Crf] = Crf.default
