# -*- coding: utf-8 -*-

from typing import Final
from unittest import TestCase, main

from cvp.terminal.ansi.lexer import lex_sgr_lines
from cvp.terminal.ansi.palette import TerminalPalette
from cvp.terminal.ansi.style import TerminalStyle
from cvp.terminal.ansi.tokenizer import tokenize_ansi_escape_text

_TEST_ANSI_ESCAPE_TEXT: Final[str] = (
    "\x1b[32m2000-00-00 11:22:33.444\x1b[0m \x1b[35m12345\x1b[0m/\x1b[36m138709396989\n"
    "\x1b[0m \x1b[34mCVP\x1b[0m \x1b[1mINFO\x1b[0m Current multiprocessing start\n"
    "\t  Unexpected errors"
)


class LexerTestCase(TestCase):
    def test_empty(self):
        lines = lex_sgr_lines(list())
        self.assertEqual(0, len(lines))

    def test_default(self):
        tokens = tokenize_ansi_escape_text(_TEST_ANSI_ESCAPE_TEXT)
        style = TerminalStyle()
        palette = TerminalPalette()
        lines = lex_sgr_lines(tokens, style, palette, lineno=101)
        self.assertEqual(3, len(lines))

        line1 = lines[0]
        self.assertEqual(101, line1.lineno)
        self.assertEqual(5, len(line1))
        self.assertEqual(line1[0].text, "2000-00-00 11:22:33.444")
        self.assertEqual(line1[0].style.foreground, palette.green)
        self.assertEqual(line1[1].text, " ")
        self.assertIsNone(line1[1].style.foreground)
        self.assertEqual(line1[2].text, "12345")
        self.assertEqual(line1[2].style.foreground, palette.magenta)
        self.assertEqual(line1[3].text, "/")
        self.assertIsNone(line1[3].style.foreground)
        self.assertEqual(line1[4].text, "138709396989")
        self.assertEqual(line1[4].style.foreground, palette.cyan)
        self.assertTrue(all(t.error is None for t in line1))

        line2 = lines[1]
        self.assertEqual(102, line2.lineno)
        self.assertEqual(5, len(line2))
        self.assertEqual(line2[0].text, " ")
        self.assertIsNone(line2[0].style.foreground)
        self.assertEqual(line2[1].text, "CVP")
        self.assertEqual(line2[1].style.foreground, palette.blue)
        self.assertEqual(line2[2].text, " ")
        self.assertIsNone(line2[2].style.foreground)
        self.assertEqual(line2[3].text, "INFO")
        self.assertIsNone(line2[3].style.foreground)
        self.assertTrue(line2[3].style.bold)
        self.assertEqual(line2[4].text, " Current multiprocessing start")
        self.assertIsNone(line2[4].style.foreground)
        self.assertFalse(line2[4].style.bold)
        self.assertTrue(all(t.error is None for t in line2))

        line3 = lines[2]
        self.assertEqual(103, line3.lineno)
        self.assertEqual(1, len(line3))
        self.assertEqual(line3[0].text, "\t  Unexpected errors")
        self.assertIsNone(line3[0].style.foreground)
        self.assertFalse(line3[0].style.bold)
        self.assertTrue(all(t.error is None for t in line3))


if __name__ == "__main__":
    main()
