# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.capabilities.license import inspect_license


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class LicenseTestCase(TestCase):
    def test_license(self):
        license_ = inspect_license()
        self.assertTrue(license_.startswith("ffmpeg is free software"))


if __name__ == "__main__":
    main()
