# -*- coding: utf-8 -*-

from shutil import which
from unittest import TestCase, main, skipIf

from cvp.ffmpeg.structs.layouts import find_layout, find_layout_decomposition


@skipIf(not which("ffmpeg"), "Not found ffmpeg executable")
class LayoutsTestCase(TestCase):
    def test_mono(self):
        mono = find_layout("mono")
        self.assertEqual("mono", mono.name)

        decomposition = find_layout_decomposition(mono.name)
        self.assertEqual(1, len(decomposition))
        self.assertEqual("FC", decomposition[0].name)


if __name__ == "__main__":
    main()
