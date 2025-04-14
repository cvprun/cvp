# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.unicode.planes import BMP, PLANES


class PlanesTestCase(TestCase):
    def test_planes_ranges(self):
        self.assertTupleEqual((0x0000, 0xFFFF), PLANES[0].range)
        self.assertTupleEqual((0x10000, 0x1FFFF), PLANES[1].range)
        self.assertTupleEqual((0x20000, 0x2FFFF), PLANES[2].range)
        self.assertTupleEqual((0x30000, 0x3FFFF), PLANES[3].range)
        self.assertTupleEqual((0x40000, 0x4FFFF), PLANES[4].range)
        self.assertTupleEqual((0x50000, 0x5FFFF), PLANES[5].range)
        self.assertTupleEqual((0x60000, 0x6FFFF), PLANES[6].range)
        self.assertTupleEqual((0x70000, 0x7FFFF), PLANES[7].range)
        self.assertTupleEqual((0x80000, 0x8FFFF), PLANES[8].range)
        self.assertTupleEqual((0x90000, 0x9FFFF), PLANES[9].range)
        self.assertTupleEqual((0xA0000, 0xAFFFF), PLANES[10].range)
        self.assertTupleEqual((0xB0000, 0xBFFFF), PLANES[11].range)
        self.assertTupleEqual((0xC0000, 0xCFFFF), PLANES[12].range)
        self.assertTupleEqual((0xD0000, 0xDFFFF), PLANES[13].range)
        self.assertTupleEqual((0xE0000, 0xEFFFF), PLANES[14].range)
        self.assertTupleEqual((0xF0000, 0xFFFFF), PLANES[15].range)
        self.assertTupleEqual((0x100000, 0x10FFFF), PLANES[16].range)

    def test_split_ranges(self):
        ranges = BMP.split_ranges()
        self.assertTupleEqual((0x0000, 0x00FF), ranges[0])
        self.assertTupleEqual((0x0100, 0x01FF), ranges[1])
        self.assertTupleEqual((0xFE00, 0xFEFF), ranges[-2])
        self.assertTupleEqual((0xFF00, 0xFFFF), ranges[-1])

    def test_contains(self):
        self.assertTrue(BMP.contain(0x0000))
        self.assertTrue(BMP.contain(0xFFFF))

        self.assertTrue(BMP.contain(0x0000 + 1))
        self.assertTrue(BMP.contain(0xFFFF - 1))

        self.assertFalse(BMP.contain(0x0000 - 1))
        self.assertFalse(BMP.contain(0xFFFF + 1))


if __name__ == "__main__":
    main()
