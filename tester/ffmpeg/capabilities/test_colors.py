# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.capabilities.colors import find_color


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class ColorsTestCase(TestCase):
    def test_gray(self):
        gray = find_color("Gray")
        self.assertEqual("Gray", gray.name)
        self.assertEqual("#808080", gray.color)


if __name__ == "__main__":
    main()
