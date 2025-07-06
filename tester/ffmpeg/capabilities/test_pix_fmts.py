# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.capabilities.pix_fmts import find_pix_fmt


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class PixFmtsTestCase(TestCase):
    def test_yuv420p(self):
        yuv420p = find_pix_fmt("yuv420p")
        self.assertEqual("yuv420p", yuv420p.name)


if __name__ == "__main__":
    main()
