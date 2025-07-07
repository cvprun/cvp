# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.capabilities.dispositions import inspect_dispositions
from cvp.ffmpeg.capabilities.version import inspect_version


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class DispositionsTestCase(TestCase):
    @skipIf(
        inspect_version("ffmpeg").major < 5,
        "Not supported in FFmpeg versions older than 5.0",
    )
    def test_default(self):
        self.assertIn("default", inspect_dispositions())


if __name__ == "__main__":
    main()
