# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Hangul_Compatibility_Jamo
# U+3130..U+318F (96 code points)

from typing import Final, Union

HANGUL_COMPATIBILITY_JAMO_BEGIN: Final[int] = 0x3130
HANGUL_COMPATIBILITY_JAMO_END: Final[int] = 0x318F


def is_hangul_compatibility_jamo_unicode(char: Union[str, int]) -> bool:
    if isinstance(char, str):
        char = ord(char)
    assert isinstance(char, int)
    return HANGUL_COMPATIBILITY_JAMO_BEGIN <= char <= HANGUL_COMPATIBILITY_JAMO_END
