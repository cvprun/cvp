# -*- coding: utf-8 -*-

from typing import Final
from unittest import TestCase, main

from cvp.terminal.ansi.parser import parse_ansi_escape_text

_TEST_ANSI_ESCAPE_TEXT: Final[str] = (
    "\x1b[32m2000-00-00 11:22:33.444\x1b[0m \x1b[35m12345\x1b[0m/\x1b[36m13870939698928"
    "\x1b[0m \x1b[34mCVP\x1b[0m \x1b[1mINFO\x1b[0m Current multiprocessing start method"
)


class ParserTestCase(TestCase):
    def test_default(self):
        tokens = parse_ansi_escape_text(_TEST_ANSI_ESCAPE_TEXT)
        self.assertEqual(20, len(tokens))

        self.assertEqual(tokens[0].token, "\x1b[32m")
        self.assertEqual(tokens[1].token, "2000-00-00 11:22:33.444")
        self.assertEqual(tokens[2].token, "\x1b[0m")
        self.assertEqual(tokens[3].token, " ")
        self.assertEqual(tokens[4].token, "\x1b[35m")
        self.assertEqual(tokens[5].token, "12345")
        self.assertEqual(tokens[6].token, "\x1b[0m")
        self.assertEqual(tokens[7].token, "/")
        self.assertEqual(tokens[8].token, "\x1b[36m")
        self.assertEqual(tokens[9].token, "13870939698928")

        self.assertEqual(tokens[10].token, "\x1b[0m")
        self.assertEqual(tokens[11].token, " ")
        self.assertEqual(tokens[12].token, "\x1b[34m")
        self.assertEqual(tokens[13].token, "CVP")
        self.assertEqual(tokens[14].token, "\x1b[0m")
        self.assertEqual(tokens[15].token, " ")
        self.assertEqual(tokens[16].token, "\x1b[1m")
        self.assertEqual(tokens[17].token, "INFO")
        self.assertEqual(tokens[18].token, "\x1b[0m")
        self.assertEqual(tokens[19].token, " Current multiprocessing start method")


if __name__ == "__main__":
    main()
