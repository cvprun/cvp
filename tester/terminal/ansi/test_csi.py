# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.encoding import ascii
from cvp.terminal.ansi.csi import (
    is_final_byte,
    is_intermediate_bytes,
    is_parameter_bytes,
    parse_csi_command,
)


class CsiTestCase(TestCase):
    def test_prefix_errors(self):
        with self.assertRaises(ValueError):
            parse_csi_command("")
        with self.assertRaises(ValueError):
            parse_csi_command("[")
        with self.assertRaises(ValueError):
            parse_csi_command("\x1b")
        with self.assertRaises(ValueError):
            parse_csi_command("\x1b?")
        with self.assertRaises(ValueError):
            parse_csi_command("\x1b[")
        with self.assertRaises(ValueError):
            parse_csi_command("\x1b[\t")

    def test_sgr_command(self):
        text = "\x1b[1;2;3m"
        cmd = parse_csi_command(text)
        self.assertEqual(text, cmd.full)
        self.assertEqual("1;2;3", cmd.parameter)
        self.assertEqual("", cmd.intermediate)
        self.assertEqual("m", cmd.final)
        self.assertTrue(cmd.is_sgr)
        self.assertListEqual([1, 2, 3], cmd.as_integer_parameters())

    def test_parameter_intermediate_command(self):
        text = '\x1b[1;2"p'
        cmd = parse_csi_command(text)
        self.assertEqual(text, cmd.full)
        self.assertEqual("1;2", cmd.parameter)
        self.assertEqual('"', cmd.intermediate)
        self.assertEqual("p", cmd.final)
        self.assertFalse(cmd.is_sgr)

    def test_intermediate_command(self):
        text = "\x1b[ @"
        cmd = parse_csi_command(text)
        self.assertEqual(text, cmd.full)
        self.assertEqual("", cmd.parameter)
        self.assertEqual(" ", cmd.intermediate)
        self.assertEqual("@", cmd.final)
        self.assertFalse(cmd.is_sgr)

    def test_final_command(self):
        text = "\x1b[H"
        cmd = parse_csi_command(text)
        self.assertEqual(text, cmd.full)
        self.assertEqual("", cmd.parameter)
        self.assertEqual("", cmd.intermediate)
        self.assertEqual("H", cmd.final)
        self.assertFalse(cmd.is_sgr)

    def test_intermediate_parameter_error(self):
        with self.assertRaises(ValueError):
            parse_csi_command('\x1b[" 1;2m')
        with self.assertRaises(ValueError):
            parse_csi_command("\x1b[$?25h")

    def test_cursor_commands(self):
        show_cursor_text = "\x1b[?25h"  # VT220
        show_cursor = parse_csi_command(show_cursor_text)
        self.assertEqual(show_cursor_text, show_cursor.full)
        self.assertEqual("?25", show_cursor.parameter)
        self.assertEqual("", show_cursor.intermediate)
        self.assertEqual("h", show_cursor.final)
        self.assertFalse(show_cursor.is_sgr)

        hide_cursor_text = "\x1b[?25l"
        hide_cursor = parse_csi_command(hide_cursor_text)
        self.assertEqual(hide_cursor_text, hide_cursor.full)
        self.assertEqual("?25", hide_cursor.parameter)
        self.assertEqual("", hide_cursor.intermediate)
        self.assertEqual("l", hide_cursor.final)
        self.assertFalse(hide_cursor.is_sgr)

    def test_intermediate_bytes(self):
        self.assertTrue(is_intermediate_bytes(ascii.SPACE))
        self.assertTrue(is_intermediate_bytes(ascii.EXCLAMATION_MARK))
        self.assertTrue(is_intermediate_bytes(ascii.QUOTATION_MARK))
        self.assertTrue(is_intermediate_bytes(ascii.NUMBER_SIGN))
        self.assertTrue(is_intermediate_bytes(ascii.DOLLAR_SIGN))
        self.assertTrue(is_intermediate_bytes(ascii.PERCENT_SIGN))
        self.assertTrue(is_intermediate_bytes(ascii.AMPERSAND))
        self.assertTrue(is_intermediate_bytes(ascii.APOSTROPHE))
        self.assertTrue(is_intermediate_bytes(ascii.LEFT_PARENTHESIS))
        self.assertTrue(is_intermediate_bytes(ascii.RIGHT_PARENTHESIS))
        self.assertTrue(is_intermediate_bytes(ascii.ASTERISK))
        self.assertTrue(is_intermediate_bytes(ascii.PLUS_SIGN))
        self.assertTrue(is_intermediate_bytes(ascii.COMMA))
        self.assertTrue(is_intermediate_bytes(ascii.HYPHEN_MINUS))
        self.assertTrue(is_intermediate_bytes(ascii.FULL_STOP))
        self.assertTrue(is_intermediate_bytes(ascii.SOLIDUS))

    def test_parameter_bytes(self):
        self.assertTrue(is_parameter_bytes(ascii.DIGIT_ZERO))
        self.assertTrue(is_parameter_bytes(ascii.DIGIT_ONE))
        self.assertTrue(is_parameter_bytes(ascii.DIGIT_TWO))
        self.assertTrue(is_parameter_bytes(ascii.DIGIT_THREE))
        self.assertTrue(is_parameter_bytes(ascii.DIGIT_FOUR))
        self.assertTrue(is_parameter_bytes(ascii.DIGIT_FIVE))
        self.assertTrue(is_parameter_bytes(ascii.DIGIT_SIX))
        self.assertTrue(is_parameter_bytes(ascii.DIGIT_SEVEN))
        self.assertTrue(is_parameter_bytes(ascii.DIGIT_EIGHT))
        self.assertTrue(is_parameter_bytes(ascii.DIGIT_NINE))
        self.assertTrue(is_parameter_bytes(ascii.COLON))
        self.assertTrue(is_parameter_bytes(ascii.SEMICOLON))
        self.assertTrue(is_parameter_bytes(ascii.LESS_THAN_SIGN))
        self.assertTrue(is_parameter_bytes(ascii.EQUALS_SIGN))
        self.assertTrue(is_parameter_bytes(ascii.GREATER_THAN_SIGN))
        self.assertTrue(is_parameter_bytes(ascii.QUESTION_MARK))

    def test_final_byte(self):
        self.assertTrue(is_final_byte(ascii.COMMERCIAL_AT))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_A))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_B))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_C))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_D))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_E))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_F))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_G))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_H))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_I))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_J))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_K))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_L))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_M))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_N))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_O))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_P))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_Q))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_R))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_S))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_T))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_U))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_V))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_W))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_X))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_Y))
        self.assertTrue(is_final_byte(ascii.LATIN_CAPITAL_LETTER_Z))
        self.assertTrue(is_final_byte(ascii.LEFT_SQUARE_BRACKET))
        self.assertTrue(is_final_byte(ascii.REVERSE_SOLIDUS))
        self.assertTrue(is_final_byte(ascii.RIGHT_SQUARE_BRACKET))
        self.assertTrue(is_final_byte(ascii.CIRCUMFLEX_ACCENT))
        self.assertTrue(is_final_byte(ascii.LOW_LINE))
        self.assertTrue(is_final_byte(ascii.GRAVE_ACCENT))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_A))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_B))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_C))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_D))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_E))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_F))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_G))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_H))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_I))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_J))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_K))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_L))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_M))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_N))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_O))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_P))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_Q))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_R))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_S))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_T))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_U))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_V))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_W))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_X))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_Y))
        self.assertTrue(is_final_byte(ascii.LATIN_SMALL_LETTER_Z))
        self.assertTrue(is_final_byte(ascii.LEFT_CURLY_BRACKET))
        self.assertTrue(is_final_byte(ascii.VERTICAL_LINE))
        self.assertTrue(is_final_byte(ascii.RIGHT_CURLY_BRACKET))
        self.assertTrue(is_final_byte(ascii.TILDE))


if __name__ == "__main__":
    main()
