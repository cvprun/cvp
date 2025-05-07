# -*- coding: utf-8 -*-
# https://unicode.org/Public/UNIDATA/Jamo.txt
# https://en.wikipedia.org/wiki/Hangul_Syllables
# https://ko.wikipedia.org/wiki/%ED%95%9C%EA%B8%80_%EC%9D%8C%EC%A0%88

from typing import Final, Optional, Sequence

HANGUL_CHOSEONG_KIYEOK: Final[int] = 0x1100  # G
HANGUL_CHOSEONG_SSANGKIYEOK: Final[int] = 0x1101  # GG
HANGUL_CHOSEONG_NIEUN: Final[int] = 0x1102  # N
HANGUL_CHOSEONG_TIKEUT: Final[int] = 0x1103  # D
HANGUL_CHOSEONG_SSANGTIKEUT: Final[int] = 0x1104  # DD
HANGUL_CHOSEONG_RIEUL: Final[int] = 0x1105  # R
HANGUL_CHOSEONG_MIEUM: Final[int] = 0x1106  # M
HANGUL_CHOSEONG_PIEUP: Final[int] = 0x1107  # B
HANGUL_CHOSEONG_SSANGPIEUP: Final[int] = 0x1108  # BB
HANGUL_CHOSEONG_SIOS: Final[int] = 0x1109  # S
HANGUL_CHOSEONG_SSANGSIOS: Final[int] = 0x110A  # SS
HANGUL_CHOSEONG_IEUNG: Final[int] = 0x110B  # (None)
HANGUL_CHOSEONG_CIEUC: Final[int] = 0x110C  # J
HANGUL_CHOSEONG_SSANGCIEUC: Final[int] = 0x110D  # JJ
HANGUL_CHOSEONG_CHIEUCH: Final[int] = 0x110E  # C
HANGUL_CHOSEONG_KHIEUKH: Final[int] = 0x110F  # K
HANGUL_CHOSEONG_THIEUTH: Final[int] = 0x1110  # T
HANGUL_CHOSEONG_PHIEUPH: Final[int] = 0x1111  # P
HANGUL_CHOSEONG_HIEUH: Final[int] = 0x1112  # H

HANGUL_JUNGSEONG_A: Final[int] = 0x1161  # A
HANGUL_JUNGSEONG_AE: Final[int] = 0x1162  # AE
HANGUL_JUNGSEONG_YA: Final[int] = 0x1163  # YA
HANGUL_JUNGSEONG_YAE: Final[int] = 0x1164  # YAE
HANGUL_JUNGSEONG_EO: Final[int] = 0x1165  # EO
HANGUL_JUNGSEONG_E: Final[int] = 0x1166  # E
HANGUL_JUNGSEONG_YEO: Final[int] = 0x1167  # YEO
HANGUL_JUNGSEONG_YE: Final[int] = 0x1168  # YE
HANGUL_JUNGSEONG_O: Final[int] = 0x1169  # O
HANGUL_JUNGSEONG_WA: Final[int] = 0x116A  # WA
HANGUL_JUNGSEONG_WAE: Final[int] = 0x116B  # WAE
HANGUL_JUNGSEONG_OE: Final[int] = 0x116C  # OE
HANGUL_JUNGSEONG_YO: Final[int] = 0x116D  # YO
HANGUL_JUNGSEONG_U: Final[int] = 0x116E  # U
HANGUL_JUNGSEONG_WEO: Final[int] = 0x116F  # WEO
HANGUL_JUNGSEONG_WE: Final[int] = 0x1170  # WE
HANGUL_JUNGSEONG_WI: Final[int] = 0x1171  # WI
HANGUL_JUNGSEONG_YU: Final[int] = 0x1172  # YU
HANGUL_JUNGSEONG_EU: Final[int] = 0x1173  # EU
HANGUL_JUNGSEONG_YI: Final[int] = 0x1174  # YI
HANGUL_JUNGSEONG_I: Final[int] = 0x1175  # I

HANGUL_JONGSEONG_KIYEOK: Final[int] = 0x11A8  # G
HANGUL_JONGSEONG_SSANGKIYEOK: Final[int] = 0x11A9  # GG
HANGUL_JONGSEONG_KIYEOK_SIOS: Final[int] = 0x11AA  # GS
HANGUL_JONGSEONG_NIEUN: Final[int] = 0x11AB  # N
HANGUL_JONGSEONG_NIEUN_CIEUC: Final[int] = 0x11AC  # NJ
HANGUL_JONGSEONG_NIEUN_HIEUH: Final[int] = 0x11AD  # NH
HANGUL_JONGSEONG_TIKEUT: Final[int] = 0x11AE  # D
HANGUL_JONGSEONG_RIEUL: Final[int] = 0x11AF  # L
HANGUL_JONGSEONG_RIEUL_KIYEOK: Final[int] = 0x11B0  # LG
HANGUL_JONGSEONG_RIEUL_MIEUM: Final[int] = 0x11B1  # LM
HANGUL_JONGSEONG_RIEUL_PIEUP: Final[int] = 0x11B2  # LB
HANGUL_JONGSEONG_RIEUL_SIOS: Final[int] = 0x11B3  # LS
HANGUL_JONGSEONG_RIEUL_THIEUTH: Final[int] = 0x11B4  # LT
HANGUL_JONGSEONG_RIEUL_PHIEUPH: Final[int] = 0x11B5  # LP
HANGUL_JONGSEONG_RIEUL_HIEUH: Final[int] = 0x11B6  # LH
HANGUL_JONGSEONG_MIEUM: Final[int] = 0x11B7  # M
HANGUL_JONGSEONG_PIEUP: Final[int] = 0x11B8  # B
HANGUL_JONGSEONG_PIEUP_SIOS: Final[int] = 0x11B9  # BS
HANGUL_JONGSEONG_SIOS: Final[int] = 0x11BA  # S
HANGUL_JONGSEONG_SSANGSIOS: Final[int] = 0x11BB  # SS
HANGUL_JONGSEONG_IEUNG: Final[int] = 0x11BC  # NG
HANGUL_JONGSEONG_CIEUC: Final[int] = 0x11BD  # J
HANGUL_JONGSEONG_CHIEUCH: Final[int] = 0x11BE  # C
HANGUL_JONGSEONG_KHIEUKH: Final[int] = 0x11BF  # K
HANGUL_JONGSEONG_THIEUTH: Final[int] = 0x11C0  # T
HANGUL_JONGSEONG_PHIEUPH: Final[int] = 0x11C1  # P
HANGUL_JONGSEONG_HIEUH: Final[int] = 0x11C2  # H

NONE_JONGSEONG: Final[str] = ""

HANGUL_SYLLABLES_UNICODE_BEGIN: Final[int] = 0xAC00  # '가'
HANGUL_SYLLABLES_UNICODE_END: Final[int] = 0xD7A3  # '힣'

# fmt: off
CHOSEONG: Final[Sequence[str]] = (
    "ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ",
    "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"
)
JUNGSEONG: Final[Sequence[str]] = (
    "ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ",
    "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ",
    "ㅣ"
)
CHOSEONG_COMPATIBLE_JONGSEONG: Final[Sequence[str]] = (
    NONE_JONGSEONG,
    "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ",
    "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ",
    "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"
)
# fmt: on


def combine_hangul_syllable(
    choseong: str,
    jungseong: str,
    jongseong: Optional[str] = None,
) -> str:
    if jongseong is None:
        jongseong = NONE_JONGSEONG
    assert isinstance(jongseong, str)

    choseong_index = CHOSEONG.index(choseong)
    jungseong_index = JUNGSEONG.index(jungseong)
    jongseong_index = CHOSEONG_COMPATIBLE_JONGSEONG.index(jongseong)

    offset = HANGUL_SYLLABLES_UNICODE_BEGIN
    index1 = choseong_index * len(JUNGSEONG) * len(CHOSEONG_COMPATIBLE_JONGSEONG)
    index2 = jungseong_index * len(CHOSEONG_COMPATIBLE_JONGSEONG)
    index3 = jongseong_index

    return chr(offset + index1 + index2 + index3)
