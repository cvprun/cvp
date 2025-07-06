# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.structs.devices import find_device


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class DevicesTestCase(TestCase):
    def test_lavfi(self):
        lavfi = find_device("lavfi")
        self.assertEqual("lavfi", lavfi.name)


if __name__ == "__main__":
    main()
