# -*- coding: utf-8 -*-

from unittest import TestCase, main

import numpy as np

from cvp.maths.statistics.clustering.ious.numpy import calculate_iou


class IouNumpyTestCase(TestCase):
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
        seg1 = np.zeros((10, 10), dtype=bool)
        seg2 = np.zeros((10, 10), dtype=bool)

        seg1[1:6, 1:6] = True
        seg2[3:9, 3:9] = True

        self.assertEqual(25, np.count_nonzero(seg1))
        self.assertEqual(36, np.count_nonzero(seg2))

        self.assertEqual(9, np.logical_and(seg1, seg2).sum())
        self.assertEqual(25 + 36 - 9, np.logical_or(seg1, seg2).sum())

        self.assertAlmostEqual(0.173, calculate_iou(seg1, seg2), 3)


if __name__ == "__main__":
    main()
