# -*- coding: utf-8 -*-

from typing import Final, Optional, Sequence, Tuple

from cvp.unicode.hangul.compatibility_jamo import MODERN_CHOSEONG as _CHOSEONG
from cvp.unicode.hangul.compatibility_jamo import MODERN_JONGSEONG_AS_CHOSEONG
from cvp.unicode.hangul.compatibility_jamo import MODERN_JUNGSEONG as _JUNGSEONG
from cvp.unicode.hangul.syllables import (
    HANGUL_SYLLABLES_BEGIN,
    HANGUL_SYLLABLES_END,
    is_hangul_syllables_unicode,
)

_EMPTY_CHAR: Final[str] = str()
_NONE_JONGSEONG: Final[str] = str()

_HANGUL_SYLLABLES_OFFSET: Final[int] = HANGUL_SYLLABLES_BEGIN
_HANGUL_SYLLABLES_SIZE: Final[int] = HANGUL_SYLLABLES_END - HANGUL_SYLLABLES_BEGIN + 1

_JONGSEONG: Final[Sequence[str]] = _NONE_JONGSEONG, *MODERN_JONGSEONG_AS_CHOSEONG

_CHOSEONG_LEN: Final[int] = len(_CHOSEONG)
_JUNGSEONG_LEN: Final[int] = len(_JUNGSEONG)
_JONGSEONG_LEN: Final[int] = len(_JONGSEONG)

MODERN_JONGSEONG_AS_CHOSEONG_WITH_NONE: Final[Sequence[str]] = _JONGSEONG


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


def get_hangul_syllable_index(hangul_char: str) -> int:
    if not is_hangul_syllables_unicode(hangul_char):
        raise ValueError(f"'{hangul_char}' is not hangul syllables unicode")

    return ord(hangul_char) - HANGUL_SYLLABLES_BEGIN


def get_hangul_compatibility_jamo_indexes(hangul_char: str) -> Tuple[int, int, int]:
    index = get_hangul_syllable_index(hangul_char)
    assert 0 <= index < _HANGUL_SYLLABLES_SIZE

    jongseong_index = int(index % _JONGSEONG_LEN)
    index //= _JONGSEONG_LEN

    jungseong_index = int(index % _JUNGSEONG_LEN)
    index //= _JUNGSEONG_LEN

    choseong_index = int(index)

    return choseong_index, jungseong_index, jongseong_index


def decompose_hangul_syllable(hangul_char: str) -> Tuple[str, str, str]:
    if 1 != len(hangul_char):
        raise ValueError("Only one character must be specified")
    cho, jung, jong = get_hangul_compatibility_jamo_indexes(hangul_char)
    return _CHOSEONG[cho], _JUNGSEONG[jung], _JONGSEONG[jong]
