# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.ime.sources.hangul.dubeolsik.syllable import DubeolsikHangulSyllable


class SyllableTestCase(TestCase):
    def test_unpacking(self):
        syllable = DubeolsikHangulSyllable()

        syllable.push("ㅎ")
        syllable.push("ㅏ")
        syllable.push("ㄴ")

        cho, jung, jong = syllable
        self.assertEqual("ㅎ", cho)
        self.assertEqual("ㅏ", jung)
        self.assertEqual("ㄴ", jong)

    def test_sample_complex_char(self):
        syllable = DubeolsikHangulSyllable()

        self.assertSequenceEqual((), syllable.push("ㄲ"))
        self.assertEqual("ㄲ", syllable.choseong)
        self.assertIsNone(syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("ㄲ", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㅜ"))
        self.assertEqual("ㄲ", syllable.choseong)
        self.assertEqual("ㅜ", syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("꾸", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㅔ"))
        self.assertEqual("ㄲ", syllable.choseong)
        self.assertEqual("ㅞ", syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("꿰", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㄹ"))
        self.assertEqual("ㄲ", syllable.choseong)
        self.assertEqual("ㅞ", syllable.jungseong)
        self.assertEqual("ㄹ", syllable.jongseong)
        self.assertEqual("꿸", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㅎ"))
        self.assertEqual("ㄲ", syllable.choseong)
        self.assertEqual("ㅞ", syllable.jungseong)
        self.assertEqual("ㅀ", syllable.jongseong)
        self.assertEqual("꿿", syllable.compose())

        self.assertSequenceEqual(("꿸",), syllable.push("ㅗ"))
        self.assertEqual("ㅎ", syllable.choseong)
        self.assertEqual("ㅗ", syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("호", syllable.compose())

    def test_sample_ga_na_da(self):
        syllable = DubeolsikHangulSyllable()

        self.assertSequenceEqual((), syllable.push("ㄱ"))
        self.assertEqual("ㄱ", syllable.choseong)
        self.assertIsNone(syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("ㄱ", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㅏ"))
        self.assertEqual("ㄱ", syllable.choseong)
        self.assertEqual("ㅏ", syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("가", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㄴ"))
        self.assertEqual("ㄱ", syllable.choseong)
        self.assertEqual("ㅏ", syllable.jungseong)
        self.assertEqual("ㄴ", syllable.jongseong)
        self.assertEqual("간", syllable.compose())

        self.assertSequenceEqual(("가",), syllable.push("ㅏ"))
        self.assertEqual("ㄴ", syllable.choseong)
        self.assertEqual("ㅏ", syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("나", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㄷ"))
        self.assertEqual("ㄴ", syllable.choseong)
        self.assertEqual("ㅏ", syllable.jungseong)
        self.assertEqual("ㄷ", syllable.jongseong)
        self.assertEqual("낟", syllable.compose())

        self.assertSequenceEqual(("나",), syllable.push("ㅏ"))
        self.assertEqual("ㄷ", syllable.choseong)
        self.assertEqual("ㅏ", syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("다", syllable.compose())

        self.assertSequenceEqual(("다", "."), syllable.push("."))
        self.assertIsNone(syllable.choseong)
        self.assertIsNone(syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("", syllable.compose())

    def test_sample_hangul(self):
        syllable = DubeolsikHangulSyllable()

        self.assertSequenceEqual((), syllable.push("ㅎ"))
        self.assertEqual("ㅎ", syllable.choseong)
        self.assertIsNone(syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("ㅎ", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㅏ"))
        self.assertEqual("ㅎ", syllable.choseong)
        self.assertEqual("ㅏ", syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("하", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㄴ"))
        self.assertEqual("ㅎ", syllable.choseong)
        self.assertEqual("ㅏ", syllable.jungseong)
        self.assertEqual("ㄴ", syllable.jongseong)
        self.assertEqual("한", syllable.compose())

        self.assertSequenceEqual(("한",), syllable.push("ㄱ"))
        self.assertEqual("ㄱ", syllable.choseong)
        self.assertIsNone(syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("ㄱ", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㅡ"))
        self.assertEqual("ㄱ", syllable.choseong)
        self.assertEqual("ㅡ", syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("그", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㄹ"))
        self.assertEqual("ㄱ", syllable.choseong)
        self.assertEqual("ㅡ", syllable.jungseong)
        self.assertEqual("ㄹ", syllable.jongseong)
        self.assertEqual("글", syllable.compose())

        self.assertSequenceEqual(("글", "."), syllable.push("."))
        self.assertIsNone(syllable.choseong)
        self.assertIsNone(syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("", syllable.compose())

    def test_only_jungseong(self):
        syllable = DubeolsikHangulSyllable()

        self.assertSequenceEqual((), syllable.push("ㅡ"))
        self.assertIsNone(syllable.choseong)
        self.assertEqual("ㅡ", syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("ㅡ", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㅣ"))
        self.assertIsNone(syllable.choseong)
        self.assertEqual("ㅢ", syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("ㅢ", syllable.compose())

        self.assertSequenceEqual(("ㅢ",), syllable.push("ㅡ"))
        self.assertIsNone(syllable.choseong)
        self.assertEqual("ㅡ", syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("ㅡ", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㅣ"))
        self.assertIsNone(syllable.choseong)
        self.assertEqual("ㅢ", syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("ㅢ", syllable.compose())

        self.assertEqual("ㅣ", syllable.pop())
        self.assertEqual("ㅡ", syllable.compose())

        self.assertEqual("ㅡ", syllable.pop())
        self.assertEqual("", syllable.compose())

        self.assertIsNone(syllable.pop())

        self.assertFalse(syllable)

    def test_only_choseong(self):
        syllable = DubeolsikHangulSyllable()

        self.assertSequenceEqual((), syllable.push("ㄹ"))
        self.assertEqual("ㄹ", syllable.choseong)
        self.assertIsNone(syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("ㄹ", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㄱ"))
        self.assertIsNone(syllable.choseong)
        self.assertIsNone(syllable.jungseong)
        self.assertEqual("ㄺ", syllable.jongseong)
        self.assertEqual("ㄺ", syllable.compose())

        self.assertSequenceEqual(("ㄺ",), syllable.push("ㄹ"))
        self.assertEqual("ㄹ", syllable.choseong)
        self.assertIsNone(syllable.jungseong)
        self.assertIsNone(syllable.jongseong)
        self.assertEqual("ㄹ", syllable.compose())

        self.assertSequenceEqual((), syllable.push("ㄱ"))
        self.assertIsNone(syllable.choseong)
        self.assertIsNone(syllable.jungseong)
        self.assertEqual("ㄺ", syllable.jongseong)
        self.assertEqual("ㄺ", syllable.compose())

        self.assertEqual("ㄱ", syllable.pop())
        self.assertEqual("ㄹ", syllable.compose())

        self.assertEqual("ㄹ", syllable.pop())
        self.assertEqual("", syllable.compose())

        self.assertIsNone(syllable.pop())

        self.assertFalse(syllable)


if __name__ == "__main__":
    main()
