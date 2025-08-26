# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.terminal.coord import TerminalCoord
from cvp.terminal.selection import TerminalSelection


class SelectionTestCase(TestCase):
    def test_unpack(self):
        begin1 = TerminalCoord(1, 10)
        end1 = TerminalCoord(2, 3)

        begin2, end2 = TerminalSelection(end1, begin1).normalize
        self.assertEqual(begin1, begin2)
        self.assertEqual(end1, end2)

    def test_equal(self):
        begin1 = TerminalCoord(1, 10)
        end1 = TerminalCoord(3, 4)
        selection1 = TerminalSelection(begin1, end1)

        begin2 = TerminalCoord(1, 10)
        end2 = TerminalCoord(3, 4)
        selection2 = TerminalSelection(begin2, end2)

        self.assertEqual(selection1, selection2)

    def test_contain(self):
        begin = TerminalCoord(1, 10)
        end = TerminalCoord(3, 4)
        selection = TerminalSelection(begin, end)

        self.assertFalse(selection.contain_with(1, 9))
        self.assertTrue(selection.contain_with(1, 10))
        self.assertTrue(selection.contain_with(1, 11))
        self.assertTrue(selection.contain_with(2, 0))
        self.assertTrue(selection.contain_with(2, 1))
        self.assertTrue(selection.contain_with(2, 5))
        self.assertTrue(selection.contain_with(2, 11))
        self.assertTrue(selection.contain_with(3, 0))
        self.assertTrue(selection.contain_with(3, 1))
        self.assertTrue(selection.contain_with(3, 3))
        self.assertFalse(selection.contain_with(3, 4))
        self.assertFalse(selection.contain_with(3, 5))


if __name__ == "__main__":
    main()
