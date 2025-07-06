# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.structs.demuxers import find_demuxer


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class DemuxersTestCase(TestCase):
    def test_h264(self):
        h264 = find_demuxer("h264")
        self.assertEqual("h264", h264.name)


if __name__ == "__main__":
    main()
