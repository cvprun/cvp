# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Hangul_Compatibility_Jamo
# U+3130..U+318F (96 code points)

from typing import Final, Sequence, Union

HANGUL_COMPATIBILITY_JAMO_BEGIN: Final[int] = 0x3130
HANGUL_COMPATIBILITY_JAMO_END: Final[int] = 0x318F


def is_hangul_compatibility_jamo_unicode(char: Union[str, int]) -> bool:
    if isinstance(char, str):
        char = ord(char)
    assert isinstance(char, int)
    return HANGUL_COMPATIBILITY_JAMO_BEGIN <= char <= HANGUL_COMPATIBILITY_JAMO_END


# fmt: off
MODERN_CHOSEONG: Final[Sequence[str]] = (
    "ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ",
    "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"
)

MODERN_JUNGSEONG: Final[Sequence[str]] = (
    "ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ",
    "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ",
    "ㅣ"
)

MODERN_JONGSEONG_AS_CHOSEONG: Final[Sequence[str]] = (
    "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ",
    "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ",
    "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"
)
# fmt: on


def is_modern_hangul_compatibility_choseong_unicode(char: Union[str, int]) -> bool:
    if isinstance(char, str):
        char = ord(char)
    assert isinstance(char, int)
    return ord(MODERN_CHOSEONG[0]) <= char <= ord(MODERN_CHOSEONG[-1])


def is_modern_hangul_compatibility_jungseong_unicode(char: Union[str, int]) -> bool:
    if isinstance(char, str):
        char = ord(char)
    assert isinstance(char, int)
    return ord(MODERN_JUNGSEONG[0]) <= char <= ord(MODERN_JUNGSEONG[-1])


def is_modern_hangul_compatibility_jongseong_unicode(char: Union[str, int]) -> bool:
    if isinstance(char, str):
        char = ord(char)
    assert isinstance(char, int)
    return ord(MODERN_JONGSEONG_AS_CHOSEONG[0]) <= char <= ord(MODERN_JONGSEONG_AS_CHOSEONG[-1])  # noqa: E501
