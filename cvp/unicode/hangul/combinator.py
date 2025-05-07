# -*- coding: utf-8 -*-

from typing import Optional

from cvp.unicode.hangul.jamo import (
    CHOSEONG,
    CHOSEONG_COMPATIBLE_JONGSEONG,
    JUNGSEONG,
    NONE_JONGSEONG,
)
from cvp.unicode.hangul.syllables import HANGUL_SYLLABLES_BEGIN


def combine_hangul_syllable(
    choseong: str,
    jungseong: str,
    jongseong: Optional[str] = None,
    *,
    offset=HANGUL_SYLLABLES_BEGIN,
) -> str:
    if jongseong is None:
        jongseong = NONE_JONGSEONG
    assert isinstance(jongseong, str)

    choseong_index = CHOSEONG.index(choseong)
    jungseong_index = JUNGSEONG.index(jungseong)
    jongseong_index = CHOSEONG_COMPATIBLE_JONGSEONG.index(jongseong)

    index1 = choseong_index * len(JUNGSEONG) * len(CHOSEONG_COMPATIBLE_JONGSEONG)
    index2 = jungseong_index * len(CHOSEONG_COMPATIBLE_JONGSEONG)
    index3 = jongseong_index

    return chr(offset + index1 + index2 + index3)
