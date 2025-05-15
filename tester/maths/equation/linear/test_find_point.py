# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.maths.equation.linear.find_point import find_x_given_y_on_line


class FindPointTestCase(TestCase):
    def test_default(self):
        """
        6 |
        5 |       *
        4 |
        3 |    *
        2 |
        1 | *
        0 +-----------
            1  2  3
        """
        x1, y1 = 1, 1
        x2, y2 = 2, 3
        x3, y3 = 3, 5
        self.assertEqual(x3, find_x_given_y_on_line(x1, y1, x2, y2, y3))


if __name__ == "__main__":
    main()
