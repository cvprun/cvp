# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Hangul_Jamo_Extended-A
# U+A960..U+A97F (32 code points)

from typing import Final, Union

HANGUL_JAMO_EXTENDED_A_BEGIN: Final[int] = 0xA960
HANGUL_JAMO_EXTENDED_A_END: Final[int] = 0xA97F


def is_hangul_jamo_extended_a_unicode(char: Union[str, int]) -> bool:
    if isinstance(char, str):
        char = ord(char)
    assert isinstance(char, int)
    return HANGUL_JAMO_EXTENDED_A_BEGIN <= char <= HANGUL_JAMO_EXTENDED_A_END
