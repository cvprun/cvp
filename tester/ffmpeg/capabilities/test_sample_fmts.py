# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.capabilities.sample_fmts import find_sample_fmt


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class SampleFmtsTestCase(TestCase):
    def test_u8(self):
        u8 = find_sample_fmt("u8")
        self.assertEqual("u8", u8.name)


if __name__ == "__main__":
    main()
