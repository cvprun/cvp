# -*- coding: utf-8 -*-

from typing import Final
from unittest import TestCase, main

from cvp.terminal.ansi.tokenizer import (
    ESCAPE_SEQUENCE_BEGIN,
    ESCAPE_SEQUENCE_END,
    FE_ESCAPE_SEQUENCE_BEGIN,
    FE_ESCAPE_SEQUENCE_END,
    AnsiCsiEscape,
    AnsiCsiEscapeError,
    AnsiEscape,
    AnsiFeEscape,
    AnsiInvalidControlCodeError,
    AnsiLineFeed,
    AnsiNoCharError,
    AnsiRegularText,
    tokenize_ansi_escape_text,
    valid_escape_sequence,
    valid_fe_escape_sequence,
)

_TEST_ANSI_ESCAPE_TEXT: Final[str] = (
    "\x1b[32m2000-00-00 11:22:33.444\x1b[0m \x1b[35m12345\x1b[0m/\x1b[36m13870939698928"
    "\x1b[0m \x1b[34mCVP\x1b[0m \x1b[1mINFO\x1b[0m Current multiprocessing start\n"
)


class TokenizerTestCase(TestCase):
    def test_logging_text(self):
        tokens = tokenize_ansi_escape_text(_TEST_ANSI_ESCAPE_TEXT)
        self.assertEqual(21, len(tokens))

        self.assertEqual(tokens[0].text, "\x1b[32m")
        self.assertEqual(tokens[1].text, "2000-00-00 11:22:33.444")
        self.assertEqual(tokens[2].text, "\x1b[0m")
        self.assertEqual(tokens[3].text, " ")
        self.assertEqual(tokens[4].text, "\x1b[35m")
        self.assertEqual(tokens[5].text, "12345")
        self.assertEqual(tokens[6].text, "\x1b[0m")
        self.assertEqual(tokens[7].text, "/")
        self.assertEqual(tokens[8].text, "\x1b[36m")
        self.assertEqual(tokens[9].text, "13870939698928")

        self.assertEqual(tokens[10].text, "\x1b[0m")
        self.assertEqual(tokens[11].text, " ")
        self.assertEqual(tokens[12].text, "\x1b[34m")
        self.assertEqual(tokens[13].text, "CVP")
        self.assertEqual(tokens[14].text, "\x1b[0m")
        self.assertEqual(tokens[15].text, " ")
        self.assertEqual(tokens[16].text, "\x1b[1m")
        self.assertEqual(tokens[17].text, "INFO")
        self.assertEqual(tokens[18].text, "\x1b[0m")
        self.assertEqual(tokens[19].text, " Current multiprocessing start")
        self.assertEqual(tokens[20].text, "\n")

    def test_valid_escape_sequence(self):
        self.assertTrue(valid_escape_sequence(ESCAPE_SEQUENCE_BEGIN))
        self.assertTrue(valid_escape_sequence(ESCAPE_SEQUENCE_END))

        self.assertFalse(valid_escape_sequence(ESCAPE_SEQUENCE_BEGIN - 1))
        self.assertFalse(valid_escape_sequence(ESCAPE_SEQUENCE_END + 1))

        self.assertTrue(valid_escape_sequence(ord("[")))

    def test_valid_fe_escape_sequence(self):
        self.assertTrue(valid_fe_escape_sequence(FE_ESCAPE_SEQUENCE_BEGIN))
        self.assertTrue(valid_fe_escape_sequence(FE_ESCAPE_SEQUENCE_END))

        self.assertFalse(valid_fe_escape_sequence(FE_ESCAPE_SEQUENCE_BEGIN - 1))
        self.assertFalse(valid_fe_escape_sequence(FE_ESCAPE_SEQUENCE_END + 1))

        self.assertTrue(valid_fe_escape_sequence(ord("[")))

    def test_linefeed(self):
        tokens = tokenize_ansi_escape_text("\n")
        self.assertEqual(1, len(tokens))
        self.assertIsInstance(tokens[0], AnsiLineFeed)
        self.assertEqual(tokens[0].text, "\n")

    def test_middle_linefeed(self):
        tokens = tokenize_ansi_escape_text("1\n2")
        self.assertEqual(3, len(tokens))

        self.assertIsInstance(tokens[0], AnsiRegularText)
        self.assertEqual(tokens[0].text, "1")

        self.assertIsInstance(tokens[1], AnsiLineFeed)
        self.assertEqual(tokens[1].text, "\n")

        self.assertIsInstance(tokens[2], AnsiRegularText)
        self.assertEqual(tokens[2].text, "2")

    def test_no_char_error(self):
        tokens = tokenize_ansi_escape_text("\x1b")
        self.assertEqual(1, len(tokens))

        self.assertIsInstance(tokens[0], AnsiNoCharError)
        self.assertIsInstance(tokens[0], BaseException)
        self.assertEqual(tokens[0].text, "\x1b")

    def test_invalid_control_code_error(self):
        tokens = tokenize_ansi_escape_text("\x1b\x1f")
        self.assertEqual(1, len(tokens))

        self.assertIsInstance(tokens[0], AnsiInvalidControlCodeError)
        self.assertIsInstance(tokens[0], BaseException)
        self.assertEqual(tokens[0].text, "\x1b\x1f")

    def test_escape(self):
        tokens = tokenize_ansi_escape_text("\x1b\x20")
        self.assertEqual(1, len(tokens))

        self.assertIsInstance(tokens[0], AnsiEscape)
        self.assertEqual(tokens[0].text, "\x1b\x20")

    def test_fe_escape(self):
        tokens = tokenize_ansi_escape_text("\x1b\x40")
        self.assertEqual(1, len(tokens))

        self.assertIsInstance(tokens[0], AnsiFeEscape)
        self.assertEqual(tokens[0].text, "\x1b\x40")

    def test_csi_parse_error_01(self):
        tokens = tokenize_ansi_escape_text("\x1b[\x1f")
        self.assertEqual(2, len(tokens))

        self.assertIsInstance(tokens[0], AnsiCsiEscapeError)
        self.assertIsInstance(tokens[0], BaseException)
        self.assertEqual(tokens[0].text, "\x1b[")

        self.assertIsInstance(tokens[1], AnsiRegularText)
        self.assertEqual(tokens[1].text, "\x1f")

    def test_csi_parse_error_02(self):
        tokens = tokenize_ansi_escape_text("\x1b[\x1b")
        self.assertEqual(2, len(tokens))

        self.assertIsInstance(tokens[0], AnsiCsiEscapeError)
        self.assertIsInstance(tokens[0], BaseException)
        self.assertEqual(tokens[0].text, "\x1b[")

        self.assertIsInstance(tokens[1], AnsiNoCharError)
        self.assertEqual(tokens[1].text, "\x1b")

    def test_csi_escape(self):
        tokens = tokenize_ansi_escape_text("\x1b[m")
        self.assertEqual(1, len(tokens))

        self.assertIsInstance(tokens[0], AnsiCsiEscape)
        self.assertEqual(tokens[0].text, "\x1b[m")


if __name__ == "__main__":
    main()
