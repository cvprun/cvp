# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.capabilities.avoptions import find_avoptions


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class AvoptionsTestCase(TestCase):
    def test_av_codec_context(self):
        av_codec_context = find_avoptions("AVCodecContext")
        self.assertEqual("AVCodecContext", av_codec_context.name)


if __name__ == "__main__":
    main()
