# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.maths.geometry.bbox.intersection import (
    is_bbox_area_overlapping,
    is_bbox_boundary_contact,
)


class IntersectionTestCase(TestCase):
    def test_overlapping(self):
        """
        0  5  10 15 20 25
        5  .  .  .  .  .
        10 .  ┌─────┐  .
        15 .  │roi1&│  .
        20 .  └─roi2┘  .
        25 .  .  .  .  .
        """
        roi1 = 10, 10, 20, 20
        roi2 = 10, 10, 20, 20
        self.assertTrue(is_bbox_area_overlapping(roi1, roi2))
        self.assertTrue(is_bbox_boundary_contact(roi1, roi2))

    def test_separated(self):
        """
        0  5  10 15 20 25 30 35 40
        5  .  .  .  .  .  .  .  .
        10 .  .  .  .  .  ┌─────┐
        15 .  .  ┌─────┐  │roi1 │
        20 .  .  │roi2 │  └─────┘
        25 .  .  └─────┘  .  .  .
        """
        roi1 = 30, 10, 40, 20
        roi2 = 15, 15, 25, 25
        self.assertFalse(is_bbox_area_overlapping(roi1, roi2))
        self.assertFalse(is_bbox_boundary_contact(roi1, roi2))

    def test_corner_touching(self):
        """
        0  5  10 15 20 25 30
        5  .  .  .  .  .  .
        10 .  ┌─────┐  .  .
        15 .  │roi1 │  .  .
        20 .  └─────┼─────┐
        25 .  .  .  │roi2 │
        30 .  .  .  └─────┘
        """
        roi1 = 10, 10, 20, 20
        roi2 = 20, 20, 30, 30
        self.assertFalse(is_bbox_area_overlapping(roi1, roi2))
        self.assertTrue(is_bbox_boundary_contact(roi1, roi2))

    def test_edge_sharing_horizontal(self):
        """
        0  5  10 15 20 25 30
        5  .  .  .  .  .  .
        10 .  ┌─────┐  .  .
        15 .  │roi1 │  .  .
        20 .  ├─────┤  .  .
        25 .  │roi2 │  .  .
        30 .  └─────┘  .  .
        """
        roi1 = 10, 10, 20, 20
        roi2 = 10, 20, 20, 30
        self.assertFalse(is_bbox_area_overlapping(roi1, roi2))
        self.assertTrue(is_bbox_boundary_contact(roi1, roi2))

    def test_edge_sharing_vertical(self):
        """
        0  5  10 15 20 25 30
        5  .  .  .  .  .  .
        10 .  ┌─────┬─────┐
        15 .  │roi1 │roi2 │
        20 .  └─────┴─────┘
        25 .  .  .  .  .  .
        30 .  .  .  .  .  .
        """
        roi1 = 10, 10, 20, 20
        roi2 = 20, 10, 30, 20
        self.assertFalse(is_bbox_area_overlapping(roi1, roi2))
        self.assertTrue(is_bbox_boundary_contact(roi1, roi2))

    def test_partial_overlap(self):
        """
        0  5  10 15 20 25 30 35
        5  .  .  .  .  .  .  .
        10 .  ┌────────┐  .  .
        15 .  │roi1    │  .  .
        20 .  │     ┌──┼─────┐
        25 .  └─────┼──┘     │
        30 .  .  .  │    roi2│
        35 .  .  .  └────────┘
        """
        roi1 = 10, 10, 25, 25
        roi2 = 20, 20, 35, 35
        self.assertTrue(is_bbox_area_overlapping(roi1, roi2))
        self.assertTrue(is_bbox_boundary_contact(roi1, roi2))

    def test_containment(self):
        """
        0  5  10 15 20 25 30 35
        5  .  .  .  .  .  .  .
        10 .  ┌──────────────┐
        15 .  │  ┌─────┐     │
        20 .  │  │roi2 │     │
        25 .  │  └─────┘     │
        30 .  │         roi1 │
        35 .  └──────────────┘
        """
        roi1 = 10, 10, 35, 35
        roi2 = 15, 15, 25, 25
        self.assertTrue(is_bbox_area_overlapping(roi1, roi2))
        self.assertTrue(is_bbox_boundary_contact(roi1, roi2))


if __name__ == "__main__":
    main()
