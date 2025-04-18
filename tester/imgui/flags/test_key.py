# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.imgui.flags.key import KeyFlags


class KeyTestCase(TestCase):
    def test_name(self):
        self.assertEqual("none", KeyFlags(0).name)


if __name__ == "__main__":
    main()
