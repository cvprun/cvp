# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.maths.geometry.bbox.normalize import normalize_bbox


class NormalizeTestCase(TestCase):
    def test_normalize_bbox(self):
        self.assertTupleEqual((0, 0, 1, 1), normalize_bbox((0, 0, 1, 1)))
        self.assertTupleEqual((0, 0, 1, 1), normalize_bbox((1, 1, 0, 0)))

        self.assertTupleEqual((1, 2, 1, 2), normalize_bbox((1, 2, 1, 2)))
        self.assertTupleEqual((2, 1, 2, 1), normalize_bbox((2, 1, 2, 1)))


if __name__ == "__main__":
    main()
