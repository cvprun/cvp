# -*- coding: utf-8 -*-

from typing import Final
from unittest import TestCase, main

from cvp.terminal.ansi.sgr.builder import SgrBuilder

_TEST_ANSI_ESCAPE_TEXT: Final[str] = (
    "\x1b[32m2000-00-00 11:22:33.444\x1b[0m \x1b[35m12345\x1b[0m/\x1b[36mAB\n"
    "\x1b[0m \x1b[34mCVP\x1b[0m \x1b[1mINFO\x1b[0m\tCurrent\n"
    "\t  Unexpected errors"
)


class BuilderTestCase(TestCase):
    def test_default(self):
        builder = SgrBuilder(show_whitespace=True, tab_size=2)
        blocks = builder.build(_TEST_ANSI_ESCAPE_TEXT)
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


if __name__ == "__main__":
    main()
