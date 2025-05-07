# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Hangul_Jamo_Extended-B
# U+D7B0..U+D7FF (80 code points)

from typing import Final, Union

HANGUL_JAMO_EXTENDED_B_BEGIN: Final[int] = 0xD7B0
HANGUL_JAMO_EXTENDED_B_END: Final[int] = 0xD7FF


def is_hangul_jamo_extended_b_unicode(char: Union[str, int]) -> bool:
    if isinstance(char, str):
        char = ord(char)
    assert isinstance(char, int)
    return HANGUL_JAMO_EXTENDED_B_BEGIN <= char <= HANGUL_JAMO_EXTENDED_B_END
