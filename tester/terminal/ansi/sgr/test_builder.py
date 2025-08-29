# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import Final
from unittest import TestCase, main

from cvp.terminal.ansi.sgr.builder import SgrBuilder
from cvp.terminal.selection import TerminalSelection
from cvp.terminal.style import TerminalStyle

_TEST_ANSI_ESCAPE: Final[str] = (
    "\x1b[32m2000-00-00 11:22:33.444\x1b[0m \x1b[35m12345\x1b[0m/\x1b[36mAB\n"
    "\x1b[0m \x1b[34mCVP\x1b[0m \x1b[1mINFO\x1b[0m\tCurrent\n"
    "\t  Unexpected errors"
)


class BuilderTestCase(TestCase):
    def test_build(self):
        builder = SgrBuilder(show_whitespace=True, tabsize=2)
        blocks = builder.build(1, _TEST_ANSI_ESCAPE)
        self.assertEqual(3, len(blocks))

        line1 = blocks[0]
        self.assertEqual(1, line1.lineno)
        self.assertEqual("2000-00-00 11:22:33.444 12345/AB", line1.raw_text)
        self.assertEqual("2000-00-00·11:22:33.444·12345/AB", line1.display_text)
        self.assertEqual(1, line1.col_begin)
        self.assertEqual(33, line1.col_end)
        self.assertEqual(32, line1.cols)
        self.assertEqual(7, len(line1))

        line2 = blocks[1]
        self.assertEqual(2, line2.lineno)
        self.assertEqual(" CVP INFO\tCurrent", line2.raw_text)
        self.assertEqual("·CVP·INFO» Current", line2.display_text)
        self.assertEqual(1, line2.col_begin)
        self.assertEqual(19, line2.col_end)
        self.assertEqual(18, line2.cols)
        self.assertEqual(6, len(line2))

        line3 = blocks[2]
        self.assertEqual(3, line3.lineno)
        self.assertEqual("\t  Unexpected errors", line3.raw_text)
        self.assertEqual("» ··Unexpected·errors", line3.display_text)
        self.assertEqual(1, line3.col_begin)
        self.assertEqual(22, line3.col_end)
        self.assertEqual(21, line3.cols)
        self.assertEqual(4, len(line3))

    def test_build_with_selection(self):
        builder = SgrBuilder(show_whitespace=True, tabsize=2)
        selection = TerminalSelection.from_raw(2, 8, 3, 6)
        blocks = builder.build(1, _TEST_ANSI_ESCAPE, selection=selection)
        self.assertEqual(3, len(blocks))

        line1 = blocks[0]
        self.assertEqual(1, line1.lineno)
        self.assertEqual(7, len(line1))
        self.assertIsNone(line1.get_selected_col_begin())
        self.assertIsNone(line1.get_selected_col_end())
        self.assertEqual("", line1.selected_raw_text)
        self.assertEqual("", line1.selected_display_text)

        line2 = blocks[1]
        self.assertEqual(2, line2.lineno)
        self.assertEqual(7, len(line2))
        self.assertEqual(8, line2.get_selected_col_begin())
        self.assertEqual(19, line2.get_selected_col_end())
        self.assertEqual("FO\tCurrent", line2.selected_raw_text)
        self.assertEqual("FO» Current", line2.selected_display_text)

        line3 = blocks[2]
        self.assertEqual(3, line3.lineno)
        self.assertEqual(5, len(line3))
        self.assertEqual(1, line3.get_selected_col_begin())
        self.assertEqual(6, line3.get_selected_col_end())
        self.assertEqual("\t  U", line3.selected_raw_text)
        self.assertEqual("» ··U", line3.selected_display_text)

    def test_build_with_line_selection(self):
        builder = SgrBuilder(show_whitespace=True, tabsize=2)
        selection = TerminalSelection.from_lineno(2)
        blocks = builder.build(1, _TEST_ANSI_ESCAPE, selection=selection)
        self.assertEqual(3, len(blocks))

        line1 = blocks[0]
        self.assertEqual(1, line1.lineno)
        self.assertEqual(7, len(line1))
        self.assertIsNone(line1.get_selected_col_begin())
        self.assertIsNone(line1.get_selected_col_end())
        self.assertEqual("", line1.selected_raw_text)
        self.assertEqual("", line1.selected_display_text)

        line2 = blocks[1]
        self.assertEqual(2, line2.lineno)
        self.assertEqual(6, len(line2))
        self.assertEqual(1, line2.get_selected_col_begin())
        self.assertEqual(19, line2.get_selected_col_end())
        self.assertEqual(" CVP INFO\tCurrent", line2.selected_raw_text)
        self.assertEqual("·CVP·INFO» Current", line2.selected_display_text)

        line3 = blocks[2]
        self.assertEqual(3, line3.lineno)
        self.assertEqual(4, len(line3))
        self.assertIsNone(line3.get_selected_col_begin())
        self.assertIsNone(line3.get_selected_col_end())
        self.assertEqual("", line3.selected_raw_text)
        self.assertEqual("", line3.selected_display_text)

    def test_get_cached_line(self):
        style = TerminalStyle(bold=True)
        selection = TerminalSelection.from_raw(100, 10, 100, 40)
        style_before = deepcopy(style)
        self.assertEqual(style, style_before)

        builder = SgrBuilder(show_whitespace=True, tabsize=2)
        cache = builder.get_cached_line(
            100,
            _TEST_ANSI_ESCAPE,
            style,
            selection=selection,
            same_line=True,
        )
        self.assertEqual(100, cache.lineno)
        self.assertEqual(_TEST_ANSI_ESCAPE, cache.text)

        self.assertEqual(style_before, cache.style_before)
        self.assertNotEqual(style_before, style)

        self.assertEqual(100, cache.line.lineno)
        self.assertEqual(1, cache.col_begin)
        self.assertEqual(72, cache.col_end)
        self.assertEqual(10, cache.selected_col_begin)
        self.assertEqual(40, cache.selected_col_end)

        expect_raw_text = (
            "2000-00-00 11:22:33.444 12345/AB"
            " CVP INFO\tCurrent"
            "\t  Unexpected errors"
        )
        self.assertEqual(expect_raw_text, cache.line.raw_text)

        expect_display_text = (
            "2000-00-00·11:22:33.444·12345/AB"
            "·CVP·INFO» Current"
            "» ··Unexpected·errors"
        )
        self.assertEqual(expect_display_text, cache.line.display_text)


if __name__ == "__main__":
    main()
