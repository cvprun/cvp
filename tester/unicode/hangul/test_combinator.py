# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.unicode.hangul.combinator import (
    MODERN_JONGSEONG_AS_CHOSEONG_WITH_NONE,
    compose_hangul_syllable,
)
from cvp.unicode.hangul.compatibility_jamo import MODERN_CHOSEONG, MODERN_JUNGSEONG
from cvp.unicode.hangul.syllables import HANGUL_SYLLABLES_BEGIN, HANGUL_SYLLABLES_END


class CombinatorTestCase(TestCase):
    def test_sample_hangul(self):
        self.assertEqual("한", compose_hangul_syllable("ㅎ", "ㅏ", "ㄴ"))
        self.assertEqual("글", compose_hangul_syllable("ㄱ", "ㅡ", "ㄹ"))

        hangul_begin = chr(HANGUL_SYLLABLES_BEGIN)
        hangul_end = chr(HANGUL_SYLLABLES_END)

        self.assertEqual(hangul_begin, compose_hangul_syllable("ㄱ", "ㅏ"))
        self.assertEqual(hangul_end, compose_hangul_syllable("ㅎ", "ㅣ", "ㅎ"))

    def test_combine_hangul_syllable(self):
        args = list()
        for cho in MODERN_CHOSEONG:
            for jung in MODERN_JUNGSEONG:
                for jong in MODERN_JONGSEONG_AS_CHOSEONG_WITH_NONE:
                    args.append((cho, jung, jong))

        size = HANGUL_SYLLABLES_END - HANGUL_SYLLABLES_BEGIN + 1
        self.assertEqual(size, len(args))

        codes = [HANGUL_SYLLABLES_BEGIN + index for index in range(size)]
        self.assertEqual(HANGUL_SYLLABLES_BEGIN, codes[0])
        self.assertEqual(HANGUL_SYLLABLES_END, codes[-1])

        result = [ord(compose_hangul_syllable(*a)) == c for a, c in zip(args, codes)]
        self.assertTrue(all(result))


if __name__ == "__main__":
    main()
