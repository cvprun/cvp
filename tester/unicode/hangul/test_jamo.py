# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.unicode.hangul import compatibility_jamo as c_jamo
from cvp.unicode.hangul import jamo


class JamoTestCase(TestCase):
    def test_choseong(self):
        j_choseong = jamo.MODERN_HANGUL_CHOSEONG
        c_choseong = c_jamo.MODERN_CHOSEONG
        self.assertEqual(len(j_choseong), len(c_choseong))

        def get_jamo(char: str):
            return c_choseong.index(char) + j_choseong[0]

        self.assertEqual(get_jamo("ㄱ"), jamo.HANGUL_CHOSEONG_KIYEOK)
        self.assertEqual(get_jamo("ㄲ"), jamo.HANGUL_CHOSEONG_SSANGKIYEOK)
        self.assertEqual(get_jamo("ㄴ"), jamo.HANGUL_CHOSEONG_NIEUN)
        self.assertEqual(get_jamo("ㄷ"), jamo.HANGUL_CHOSEONG_TIKEUT)
        self.assertEqual(get_jamo("ㄸ"), jamo.HANGUL_CHOSEONG_SSANGTIKEUT)
        self.assertEqual(get_jamo("ㄹ"), jamo.HANGUL_CHOSEONG_RIEUL)
        self.assertEqual(get_jamo("ㅁ"), jamo.HANGUL_CHOSEONG_MIEUM)
        self.assertEqual(get_jamo("ㅂ"), jamo.HANGUL_CHOSEONG_PIEUP)
        self.assertEqual(get_jamo("ㅃ"), jamo.HANGUL_CHOSEONG_SSANGPIEUP)
        self.assertEqual(get_jamo("ㅅ"), jamo.HANGUL_CHOSEONG_SIOS)
        self.assertEqual(get_jamo("ㅆ"), jamo.HANGUL_CHOSEONG_SSANGSIOS)
        self.assertEqual(get_jamo("ㅇ"), jamo.HANGUL_CHOSEONG_IEUNG)
        self.assertEqual(get_jamo("ㅈ"), jamo.HANGUL_CHOSEONG_CIEUC)
        self.assertEqual(get_jamo("ㅉ"), jamo.HANGUL_CHOSEONG_SSANGCIEUC)
        self.assertEqual(get_jamo("ㅊ"), jamo.HANGUL_CHOSEONG_CHIEUCH)
        self.assertEqual(get_jamo("ㅋ"), jamo.HANGUL_CHOSEONG_KHIEUKH)
        self.assertEqual(get_jamo("ㅌ"), jamo.HANGUL_CHOSEONG_THIEUTH)
        self.assertEqual(get_jamo("ㅍ"), jamo.HANGUL_CHOSEONG_PHIEUPH)
        self.assertEqual(get_jamo("ㅎ"), jamo.HANGUL_CHOSEONG_HIEUH)

    def test_jungseong(self):
        j_jungseong = jamo.MODERN_HANGUL_JUNGSEONG
        c_jungseong = c_jamo.MODERN_JUNGSEONG
        self.assertEqual(len(j_jungseong), len(c_jungseong))

        def get_jamo(char: str):
            return c_jungseong.index(char) + j_jungseong[0]

        self.assertEqual(get_jamo("ㅏ"), jamo.HANGUL_JUNGSEONG_A)
        self.assertEqual(get_jamo("ㅐ"), jamo.HANGUL_JUNGSEONG_AE)
        self.assertEqual(get_jamo("ㅑ"), jamo.HANGUL_JUNGSEONG_YA)
        self.assertEqual(get_jamo("ㅒ"), jamo.HANGUL_JUNGSEONG_YAE)
        self.assertEqual(get_jamo("ㅓ"), jamo.HANGUL_JUNGSEONG_EO)
        self.assertEqual(get_jamo("ㅔ"), jamo.HANGUL_JUNGSEONG_E)
        self.assertEqual(get_jamo("ㅕ"), jamo.HANGUL_JUNGSEONG_YEO)
        self.assertEqual(get_jamo("ㅖ"), jamo.HANGUL_JUNGSEONG_YE)
        self.assertEqual(get_jamo("ㅗ"), jamo.HANGUL_JUNGSEONG_O)
        self.assertEqual(get_jamo("ㅘ"), jamo.HANGUL_JUNGSEONG_WA)
        self.assertEqual(get_jamo("ㅙ"), jamo.HANGUL_JUNGSEONG_WAE)
        self.assertEqual(get_jamo("ㅚ"), jamo.HANGUL_JUNGSEONG_OE)
        self.assertEqual(get_jamo("ㅛ"), jamo.HANGUL_JUNGSEONG_YO)
        self.assertEqual(get_jamo("ㅜ"), jamo.HANGUL_JUNGSEONG_U)
        self.assertEqual(get_jamo("ㅝ"), jamo.HANGUL_JUNGSEONG_WEO)
        self.assertEqual(get_jamo("ㅞ"), jamo.HANGUL_JUNGSEONG_WE)
        self.assertEqual(get_jamo("ㅟ"), jamo.HANGUL_JUNGSEONG_WI)
        self.assertEqual(get_jamo("ㅠ"), jamo.HANGUL_JUNGSEONG_YU)
        self.assertEqual(get_jamo("ㅡ"), jamo.HANGUL_JUNGSEONG_EU)
        self.assertEqual(get_jamo("ㅢ"), jamo.HANGUL_JUNGSEONG_YI)
        self.assertEqual(get_jamo("ㅣ"), jamo.HANGUL_JUNGSEONG_I)

    def test_jongseong(self):
        j_jongseong = jamo.MODERN_HANGUL_JONGSEONG
        c_jongseong = c_jamo.MODERN_JONGSEONG_AS_CHOSEONG
        self.assertEqual(len(j_jongseong), len(c_jongseong))

        def get_jamo(char: str):
            return c_jongseong.index(char) + j_jongseong[0]

        self.assertEqual(get_jamo("ㄱ"), jamo.HANGUL_JONGSEONG_KIYEOK)
        self.assertEqual(get_jamo("ㄲ"), jamo.HANGUL_JONGSEONG_SSANGKIYEOK)
        self.assertEqual(get_jamo("ㄳ"), jamo.HANGUL_JONGSEONG_KIYEOK_SIOS)
        self.assertEqual(get_jamo("ㄴ"), jamo.HANGUL_JONGSEONG_NIEUN)
        self.assertEqual(get_jamo("ㄵ"), jamo.HANGUL_JONGSEONG_NIEUN_CIEUC)
        self.assertEqual(get_jamo("ㄶ"), jamo.HANGUL_JONGSEONG_NIEUN_HIEUH)
        self.assertEqual(get_jamo("ㄷ"), jamo.HANGUL_JONGSEONG_TIKEUT)
        self.assertEqual(get_jamo("ㄹ"), jamo.HANGUL_JONGSEONG_RIEUL)
        self.assertEqual(get_jamo("ㄺ"), jamo.HANGUL_JONGSEONG_RIEUL_KIYEOK)
        self.assertEqual(get_jamo("ㄻ"), jamo.HANGUL_JONGSEONG_RIEUL_MIEUM)
        self.assertEqual(get_jamo("ㄼ"), jamo.HANGUL_JONGSEONG_RIEUL_PIEUP)
        self.assertEqual(get_jamo("ㄽ"), jamo.HANGUL_JONGSEONG_RIEUL_SIOS)
        self.assertEqual(get_jamo("ㄾ"), jamo.HANGUL_JONGSEONG_RIEUL_THIEUTH)
        self.assertEqual(get_jamo("ㄿ"), jamo.HANGUL_JONGSEONG_RIEUL_PHIEUPH)
        self.assertEqual(get_jamo("ㅀ"), jamo.HANGUL_JONGSEONG_RIEUL_HIEUH)
        self.assertEqual(get_jamo("ㅁ"), jamo.HANGUL_JONGSEONG_MIEUM)
        self.assertEqual(get_jamo("ㅂ"), jamo.HANGUL_JONGSEONG_PIEUP)
        self.assertEqual(get_jamo("ㅄ"), jamo.HANGUL_JONGSEONG_PIEUP_SIOS)
        self.assertEqual(get_jamo("ㅅ"), jamo.HANGUL_JONGSEONG_SIOS)
        self.assertEqual(get_jamo("ㅆ"), jamo.HANGUL_JONGSEONG_SSANGSIOS)
        self.assertEqual(get_jamo("ㅇ"), jamo.HANGUL_JONGSEONG_IEUNG)
        self.assertEqual(get_jamo("ㅈ"), jamo.HANGUL_JONGSEONG_CIEUC)
        self.assertEqual(get_jamo("ㅊ"), jamo.HANGUL_JONGSEONG_CHIEUCH)
        self.assertEqual(get_jamo("ㅋ"), jamo.HANGUL_JONGSEONG_KHIEUKH)
        self.assertEqual(get_jamo("ㅌ"), jamo.HANGUL_JONGSEONG_THIEUTH)
        self.assertEqual(get_jamo("ㅍ"), jamo.HANGUL_JONGSEONG_PHIEUPH)
        self.assertEqual(get_jamo("ㅎ"), jamo.HANGUL_JONGSEONG_HIEUH)


if __name__ == "__main__":
    main()
