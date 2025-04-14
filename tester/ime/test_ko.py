# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.ime.ko import HangulInputHandler


class KoTestCase(TestCase):
    def test_default(self):
        handler = HangulInputHandler()
        self.assertIsNotNone(handler)


if __name__ == "__main__":
    main()
