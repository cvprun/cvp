# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class Profile(StrEnum):
    """
    HEVC/H.265 profiles

    References:
        https://trac.ffmpeg.org/wiki/Encode/H.265
        https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding#Profiles
    """

    main = auto()
    main10 = auto()
    main12 = auto()
    main422_10 = "main422-10"
    main422_12 = "main422-12"
    main444_8 = "main444-8"
    main444_10 = "main444-10"
    main444_12 = "main444-12"
    mainstillpicture = auto()
