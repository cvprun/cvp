# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.utils.version import inspect_version, parse_version_output


class VersionTestCase(TestCase):
    @skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
    def test_version(self):
        version = inspect_version()
        self.assertLessEqual(4, version.major)
        self.assertLessEqual(0, version.minor)
        self.assertLessEqual(0, version.patch)

    def test_parse_version_text_BtbN(self):
        text = "ffmpeg version n7.0.1-221-g0ab20b5788-20240731 Copyright (c) ..."
        version = parse_version_output(text)
        self.assertLessEqual(7, version.major)
        self.assertLessEqual(0, version.minor)
        self.assertLessEqual(1, version.patch)
        self.assertEqual("221-g0ab20b5788-20240731", version.extra)
        self.assertEqual("Copyright (c) ...", version.copyright_full)

    def test_parse_version_text_5x(self):
        text = "ffmpeg version 5.1.2 Copyright (c) 2000-2022 the FFmpeg developers"
        version = parse_version_output(text)
        self.assertLessEqual(5, version.major)
        self.assertLessEqual(0, version.minor)
        self.assertLessEqual(1, version.patch)
        self.assertIsNone(version.extra)
        self.assertEqual(
            "Copyright (c) 2000-2022 the FFmpeg developers",
            version.copyright_full,
        )


if __name__ == "__main__":
    main()
