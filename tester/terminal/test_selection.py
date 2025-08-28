# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.terminal.coord import TerminalCoord
from cvp.terminal.selection import TerminalSelection


class SelectionTestCase(TestCase):
    def test_unpack(self):
        begin1 = TerminalCoord(1, 10)
        end1 = TerminalCoord(2, 3)
        selection1 = TerminalSelection(begin1, end1)

        begin2, end2 = selection1.normalize
        self.assertEqual(begin1, begin2)
        self.assertEqual(end1, end2)

    def test_equal(self):
        selection1 = TerminalSelection.from_raw(1, 10, 3, 4)
        selection2 = TerminalSelection.from_raw(1, 10, 3, 4)
        self.assertEqual(selection1, selection2)

        selection3 = TerminalSelection.from_raw(2, 10, 3, 5)
        self.assertNotEqual(selection1, selection3)

    def test_contain(self):
        selection = TerminalSelection.from_raw(1, 10, 3, 4)

        self.assertNotIn((1, 9), selection)
        self.assertIn((1, 10), selection)
        self.assertIn((1, 11), selection)
        self.assertIn((2, 0), selection)
        self.assertIn((2, 1), selection)
        self.assertIn((2, 5), selection)
        self.assertIn((2, 11), selection)
        self.assertIn((3, 0), selection)
        self.assertIn((3, 1), selection)
        self.assertIn((3, 3), selection)
        self.assertNotIn((3, 4), selection)
        self.assertNotIn((3, 5), selection)

    def test_lines(self):
        selection = TerminalSelection()
        selection.set_lines(5, 10)

        self.assertNotIn(4, selection)
        self.assertIn(5, selection)
        self.assertIn(6, selection)
        self.assertIn(7, selection)
        self.assertIn(8, selection)
        self.assertIn(9, selection)
        self.assertNotIn(10, selection)

    def test_clip_with_single_line(self):
        selection = TerminalSelection.from_raw(2, 2, 2, 4)
        line2 = selection.clip(2)
        self.assertEqual((2, 2), line2.begin)
        self.assertEqual((2, 4), line2.end)

    def test_clip_with_multiple_line(self):
        selection = TerminalSelection.from_raw(2, 10, 5, 4)

        line1 = selection.clip(1)
        self.assertIsNone(line1)

        line2 = selection.clip(2)
        self.assertEqual((2, 10), line2.begin)
        self.assertEqual((3, 0), line2.end)

        line3 = selection.clip(3)
        self.assertEqual((3, 0), line3.begin)
        self.assertEqual((4, 0), line3.end)

        line4 = selection.clip(4)
        self.assertEqual((4, 0), line4.begin)
        self.assertEqual((5, 0), line4.end)

        line5 = selection.clip(5)
        self.assertEqual((5, 0), line5.begin)
        self.assertEqual((5, 4), line5.end)

        line6 = selection.clip(6)
        self.assertIsNone(line6)


if __name__ == "__main__":
    main()
