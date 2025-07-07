# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.capabilities.hwaccels import inspect_hwaccels


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class HwaccelsTestCase(TestCase):
    def test_opencl(self):
        hwaccels = inspect_hwaccels()
        self.assertIn("opencl", hwaccels)


if __name__ == "__main__":
    main()
