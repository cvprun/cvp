# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Hangul_Syllables
# https://ko.wikipedia.org/wiki/%ED%95%9C%EA%B8%80_%EC%9D%8C%EC%A0%88

from typing import Final, Union

HANGUL_SYLLABLES_BEGIN: Final[int] = 0xAC00  # '가'
HANGUL_SYLLABLES_END: Final[int] = 0xD7A3  # '힣'


def is_hangul_syllables_unicode(char: Union[str, int]) -> bool:
    if isinstance(char, str):
        char = ord(char)
    assert isinstance(char, int)
    return HANGUL_SYLLABLES_BEGIN <= char <= HANGUL_SYLLABLES_END
