# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.capabilities.bsfs import inspect_bsfs


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class BsfsTestCase(TestCase):
    def test_prefix(self):
        bsfs = inspect_bsfs()
        self.assertNotEqual(-1, bsfs.index("null"))


if __name__ == "__main__":
    main()
