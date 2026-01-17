# -*- coding: utf-8 -*-

from enum import IntEnum, unique
from typing import Final


@unique
class Crf(IntEnum):
    """
    Constant Rate Factor for AV1 (libaom-av1, libsvtav1)

    The CRF scale is 0–63, where 0 is lossless and 63 is worst quality.
    Typical values are 23-35 for good quality.

    References:
        https://trac.ffmpeg.org/wiki/Encode/AV1
    """

    lossless = 0
    high_quality = 23
    default = 30
    low_quality = 35
    worst_quality = 63
    sane_range_min = 23
    sane_range_max = 35


CRF_MIN: Final[Crf] = Crf.lossless
CRF_MAX: Final[Crf] = Crf.worst_quality
CRF_DEFAULT: Final[Crf] = Crf.default
