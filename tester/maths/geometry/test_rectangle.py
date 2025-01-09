# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.maths.geometry.rectangle import is_rectangle_collision, normalize_rectangle


class RectangleTestCase(TestCase):
    def test_normalize_rectangle(self):
        self.assertTupleEqual((0, 0, 1, 1), normalize_rectangle((0, 0, 1, 1)))
        self.assertTupleEqual((0, 0, 1, 1), normalize_rectangle((1, 1, 0, 0)))

        self.assertTupleEqual((1, 2, 1, 2), normalize_rectangle((1, 2, 1, 2)))
        self.assertTupleEqual((2, 1, 2, 1), normalize_rectangle((2, 1, 2, 1)))

    def test_is_rectangle_collision(self):
        self.assertTrue(is_rectangle_collision((10, 10, 20, 20), (15, 15, 25, 25)))
        self.assertFalse(is_rectangle_collision((30, 10, 40, 20), (15, 15, 25, 25)))

        # Exact overlap detected at corner points
        self.assertTrue(is_rectangle_collision((10, 10, 20, 20), (20, 20, 30, 30)))


if __name__ == "__main__":
    main()
