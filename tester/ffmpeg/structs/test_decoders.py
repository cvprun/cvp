# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.structs.decoders import find_decoder


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class DecodersTestCase(TestCase):
    def test_h264(self):
        h264 = find_decoder("h264")
        self.assertEqual("h264", h264.name)


if __name__ == "__main__":
    main()
