# -*- coding: utf-8 -*-

from enum import IntEnum, unique


@unique
class Tune(IntEnum):
    """
    AV1 tune options for SVT-AV1

    References:
        https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/Docs/Parameters.md
    """

    vq = 0
    """Visual quality (subjective) optimization"""

    psnr = 1
    """PSNR metric optimization"""

    ssim = 2
    """SSIM metric optimization (deprecated, same as vq)"""
