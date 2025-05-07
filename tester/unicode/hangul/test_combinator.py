# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.unicode.hangul.combinator import combine_hangul_syllable
from cvp.unicode.hangul.syllables import HANGUL_SYLLABLES_BEGIN, HANGUL_SYLLABLES_END


class CombinatorTestCase(TestCase):
    def test_combine_hangul_syllable(self):
        self.assertEqual("한", combine_hangul_syllable("ㅎ", "ㅏ", "ㄴ"))
        self.assertEqual("글", combine_hangul_syllable("ㄱ", "ㅡ", "ㄹ"))

        hangul_begin = chr(HANGUL_SYLLABLES_BEGIN)
        hangul_end = chr(HANGUL_SYLLABLES_END)

        self.assertEqual(hangul_begin, combine_hangul_syllable("ㄱ", "ㅏ"))
        self.assertEqual(hangul_end, combine_hangul_syllable("ㅎ", "ㅣ", "ㅎ"))


if __name__ == "__main__":
    main()
