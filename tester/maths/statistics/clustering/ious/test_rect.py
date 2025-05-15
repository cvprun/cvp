# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.maths.statistics.clustering.ious.rect import calculate_iou


class IouRectTestCase(TestCase):
    def test_default(self):
        """
        9 |
        8 |     @---------@
        7 |     |         |
        6 |     |         |
        5 | #---+---#     |
        4 | |   |   |     |
        3 | |   @---+-----@
        2 | |       |
        1 | #-------#
        0 +-------------------
          0 1 2 3 4 5 6 7 8 9
        """
        roi1 = 1, 1, 5, 5
        roi2 = 3, 3, 8, 8
        self.assertAlmostEqual(0.108, calculate_iou(roi1, roi2), 3)


if __name__ == "__main__":
    main()
