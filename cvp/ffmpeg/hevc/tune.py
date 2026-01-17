# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class Tune(StrEnum):
    """
    HEVC/H.265 tune options for x265

    References:
        https://x265.readthedocs.io/en/master/presets.html#tuning
    """

    psnr = auto()
    """Optimize for PSNR metric"""

    ssim = auto()
    """Optimize for SSIM metric"""

    grain = auto()
    """Preserve film grain"""

    fastdecode = auto()
    """Faster decoding"""

    zerolatency = auto()
    """Low latency streaming"""

    animation = auto()
    """Animation content"""
