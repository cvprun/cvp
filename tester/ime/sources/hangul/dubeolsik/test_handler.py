# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.ime.sources.hangul.dubeolsik.handler import DubeolsikHangulInputHandler


class HandlerTestCase(TestCase):
    def test_default(self):
        handler = DubeolsikHangulInputHandler()
        self.assertSequenceEqual((), handler.add("ㅎ"))
        self.assertEqual("ㅎ", handler.get_composing())

        self.assertSequenceEqual((), handler.add("ㅏ"))
        self.assertEqual("하", handler.get_composing())

        self.assertSequenceEqual((), handler.add("ㄴ"))
        self.assertEqual("한", handler.get_composing())

        self.assertSequenceEqual(("한",), handler.add("ㄱ"))
        self.assertEqual("ㄱ", handler.get_composing())

        self.assertSequenceEqual((), handler.add("ㅡ"))
        self.assertEqual("그", handler.get_composing())

        self.assertSequenceEqual((), handler.add("ㄹ"))
        self.assertEqual("글", handler.get_composing())

        self.assertSequenceEqual(("글", "."), handler.add("."))
        self.assertEqual("", handler.get_composing())


if __name__ == "__main__":
    main()
