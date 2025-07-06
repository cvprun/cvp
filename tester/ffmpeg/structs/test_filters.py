# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.structs.filters import find_filter


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class FiltersTestCase(TestCase):
    def test_nullsrc(self):
        nullsrc = find_filter("nullsrc")
        self.assertEqual("nullsrc", nullsrc.name)


if __name__ == "__main__":
    main()
