# -*- coding: utf-8 -*-

from typing import Final, Optional, Sequence, Union

from cvp.unicode.hangul.compatibility_jamo import MODERN_CHOSEONG as _CHOSEONG
from cvp.unicode.hangul.compatibility_jamo import MODERN_JONGSEONG_AS_CHOSEONG
from cvp.unicode.hangul.compatibility_jamo import MODERN_JUNGSEONG as _JUNGSEONG
from cvp.unicode.hangul.syllables import (
    HANGUL_SYLLABLES_BEGIN,
    HANGUL_SYLLABLES_END,
    is_hangul_syllables_unicode,
)

_NONE_JONGSEONG: Final[str] = ""

MODERN_JONGSEONG_AS_CHOSEONG_WITH_NONE: Final[Sequence[str]] = (
    _NONE_JONGSEONG, *MODERN_JONGSEONG_AS_CHOSEONG
)

_HANGUL_SYLLABLES_OFFSET: Final[int] = HANGUL_SYLLABLES_BEGIN
_CHOSEONG_LEN: Final[int] = len(_CHOSEONG)
_JUNGSEONG_LEN: Final[int] = len(_JUNGSEONG)
_JONGSEONG: Final[Sequence[str]] = MODERN_JONGSEONG_AS_CHOSEONG_WITH_NONE
_JONGSEONG_LEN: Final[int] = len(_JONGSEONG)


def compose_hangul_syllable(
    choseong: str,
    jungseong: str,
    jongseong: Optional[str] = None,
) -> str:
    if jongseong is None:
        jongseong = _NONE_JONGSEONG
    assert isinstance(jongseong, str)

    choseong_index = _CHOSEONG.index(choseong)
    jungseong_index = _JUNGSEONG.index(jungseong)
    jongseong_index = _JONGSEONG.index(jongseong)

    index1 = choseong_index * _JUNGSEONG_LEN * _JONGSEONG_LEN
    index2 = jungseong_index * _JONGSEONG_LEN
    index3 = jongseong_index

    return chr(_HANGUL_SYLLABLES_OFFSET + index1 + index2 + index3)


def hangul_syllable_index(hangul_char: str) -> int:
    if not is_hangul_syllables_unicode(hangul_char):
        raise ValueError(f"'{hangul_char}' is not hangul syllables unicode")

    return ord(hangul_char) - HANGUL_SYLLABLES_BEGIN


def decompose_hangul_syllable_index(code: int):
    if not (HANGUL_SYLLABLES_BEGIN <= code <= HANGUL_SYLLABLES_END):
        raise ValueError(f"Invalid hangul syllables code: {code}")

    jongseong_index = int(code % _JONGSEONG_LEN)
    code //= _JONGSEONG_LEN

    jungseong_index = int(code % _JUNGSEONG_LEN)
    code //= _JUNGSEONG_LEN

    choseong_index = int(code)

    return choseong_index, jungseong_index, jongseong_index
