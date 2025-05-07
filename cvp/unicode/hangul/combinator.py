# -*- coding: utf-8 -*-

from typing import Optional

from cvp.unicode.hangul.jamo import (
    MODERN_CHOSEONG,
    MODERN_JONGSEONG_AS_CHOSEONG_WITH_NONE,
    MODERN_JUNGSEONG,
    NONE_JONGSEONG,
)
from cvp.unicode.hangul.syllables import HANGUL_SYLLABLES_BEGIN, HANGUL_SYLLABLES_END


def compose_hangul_syllable(
    choseong: str,
    jungseong: str,
    jongseong: Optional[str] = None,
) -> str:
    if jongseong is None:
        jongseong = NONE_JONGSEONG
    assert isinstance(jongseong, str)

    choseong_index = MODERN_CHOSEONG.index(choseong)
    jungseong_index = MODERN_JUNGSEONG.index(jungseong)
    jongseong_index = MODERN_JONGSEONG_AS_CHOSEONG_WITH_NONE.index(jongseong)

    offset = HANGUL_SYLLABLES_BEGIN
    index1 = choseong_index * len(MODERN_JUNGSEONG) * len(MODERN_JONGSEONG_AS_CHOSEONG_WITH_NONE)
    index2 = jungseong_index * len(MODERN_JONGSEONG_AS_CHOSEONG_WITH_NONE)
    index3 = jongseong_index

    return chr(offset + index1 + index2 + index3)


def hangul_syllable_index(letter: str) -> int:
    return ord(letter) - HANGUL_SYLLABLES_BEGIN


def decompose_hangul_syllable_index(code: int):
    if not (HANGUL_SYLLABLES_BEGIN <= code <= HANGUL_SYLLABLES_END):
        raise ValueError(f"Invalid hangul syllables code: {code}")

    jongseong_index = int(code % len(MODERN_JONGSEONG_AS_CHOSEONG_WITH_NONE))
    code //= len(MODERN_JONGSEONG_AS_CHOSEONG_WITH_NONE)

    jungseong_index = int(code % len(MODERN_JUNGSEONG))
    code //= len(MODERN_JUNGSEONG)

    choseong_index = int(code)

    return choseong_index, jungseong_index, jongseong_index
