# -*- coding: utf-8 -*-

from string import ascii_letters, digits, punctuation, whitespace
from unittest import TestCase, main

from hgtk.checker import is_hangul

from cvp.ime.sources.hangul import HangulInputHandler, create_qwerty_hangul_mapping


class HangulTestCase(TestCase):
    def test_decompose(self):
        handler = HangulInputHandler()

        # noinspection SpellCheckingInspection
        self.assertEqual("ㅎㅏㄴㄱㅡㄹ", handler.decompose("한글"))

    def test_qwerty_hangul_mapping(self):
        mapping = create_qwerty_hangul_mapping()
        self.assertTrue(all([k.isalpha() for k in mapping.keys()]))
        self.assertTrue(all([is_hangul(k) for k in mapping.values()]))
        self.assertTrue(all([not is_hangul(k) for k in digits]))
        self.assertTrue(all([not is_hangul(k) for k in punctuation]))
        self.assertTrue(all([not is_hangul(k) for k in ascii_letters]))
        self.assertTrue(all([not is_hangul(k) for k in whitespace]))

    def test_add(self):
        handler = HangulInputHandler()
        self.assertSequenceEqual(("",), handler.add("ㅎ"))
        self.assertEqual("ㅎ", handler.get_composing())

        self.assertSequenceEqual(("",), handler.add("ㅏ"))
        self.assertEqual("하", handler.get_composing())

        self.assertSequenceEqual(("",), handler.add("ㄴ"))
        self.assertEqual("한", handler.get_composing())

        self.assertSequenceEqual(("한",), handler.add("ㄱ"))
        self.assertEqual("ㄱ", handler.get_composing())

        self.assertSequenceEqual(("",), handler.add("ㅡ"))
        self.assertEqual("그", handler.get_composing())

        self.assertSequenceEqual(("",), handler.add("ㄹ"))
        self.assertEqual("글", handler.get_composing())

        self.assertSequenceEqual(("글", "."), handler.add("."))
        self.assertEqual("", handler.get_composing())


if __name__ == "__main__":
    main()
