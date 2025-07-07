# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.capabilities.buildconf import startswith_build_conf


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class BuildconfTestCase(TestCase):
    def test_prefix(self):
        conf = startswith_build_conf("--prefix=")
        self.assertTrue(conf.startswith("--prefix="))


if __name__ == "__main__":
    main()
