# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.structs.formats import find_format


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class FormatsTestCase(TestCase):
    def test_mp4(self):
        mp4 = find_format("mp4")
        self.assertEqual("mp4", mp4.name)


if __name__ == "__main__":
    main()
