# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.structs.encoders import find_encoder


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class EncodersTestCase(TestCase):
    def test_libx264(self):
        libx264 = find_encoder("libx264")
        self.assertEqual("libx264", libx264.name)


if __name__ == "__main__":
    main()
