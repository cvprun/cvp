# -*- coding: utf-8 -*-

from typing import Final
from unittest import TestCase, main

from cvp.terminal.ansi.sgr.lexer import lex_sgr_lines
from cvp.terminal.ansi.sgr.parser import parse_terminal_glyphs_with_lines
from cvp.terminal.ansi.tokenizer import tokenize_ansi_escape_text
from cvp.terminal.palette import TerminalPalette
from cvp.terminal.style import TerminalStyle

_TEST_ANSI_ESCAPE_TEXT: Final[str] = "\x1b[1mINFO\x1b[0m\tCurrent\nNext"


class ParserTestCase(TestCase):
    def test_empty(self):
        lines = lex_sgr_lines(list())
        self.assertEqual(0, len(lines))

    def test_default(self):
        tokens = tokenize_ansi_escape_text(_TEST_ANSI_ESCAPE_TEXT)
        style = TerminalStyle()
        palette = TerminalPalette()
        sgr_lines = lex_sgr_lines(tokens, style, palette, lineno=101)
        glyph_lines = parse_terminal_glyphs_with_lines(sgr_lines)
        self.assertEqual(19, len(glyph_lines))
        self.assertEqual("I", glyph_lines[0].char)
        self.assertEqual("N", glyph_lines[1].char)
        self.assertEqual("F", glyph_lines[2].char)
        self.assertEqual("O", glyph_lines[3].char)
        self.assertEqual("\t", glyph_lines[4].char)
        self.assertIsNone(glyph_lines[5].char)
        self.assertIsNone(glyph_lines[6].char)
        self.assertIsNone(glyph_lines[7].char)
        self.assertEqual("C", glyph_lines[8].char)
        self.assertEqual("u", glyph_lines[9].char)
        self.assertEqual("r", glyph_lines[10].char)
        self.assertEqual("r", glyph_lines[11].char)
        self.assertEqual("e", glyph_lines[12].char)
        self.assertEqual("n", glyph_lines[13].char)
        self.assertEqual("t", glyph_lines[14].char)
        self.assertEqual("N", glyph_lines[15].char)
        self.assertEqual("e", glyph_lines[16].char)
        self.assertEqual("x", glyph_lines[17].char)
        self.assertEqual("t", glyph_lines[18].char)

        for i in range(15):
            self.assertEqual(101, glyph_lines[i].row)
            self.assertEqual(i + 1, glyph_lines[i].col)

        self.assertEqual((102, 1), glyph_lines[15].pos)
        self.assertEqual((102, 2), glyph_lines[16].pos)
        self.assertEqual((102, 3), glyph_lines[17].pos)
        self.assertEqual((102, 4), glyph_lines[18].pos)


if __name__ == "__main__":
    main()
