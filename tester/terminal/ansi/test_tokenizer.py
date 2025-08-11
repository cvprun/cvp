# -*- coding: utf-8 -*-

from typing import Final
from unittest import TestCase, main

from cvp.terminal.ansi.tokenizer import tokenize_ansi_escape_text

_TEST_ANSI_ESCAPE_TEXT: Final[str] = (
    "\x1b[32m2000-00-00 11:22:33.444\x1b[0m \x1b[35m12345\x1b[0m/\x1b[36m13870939698928"
    "\x1b[0m \x1b[34mCVP\x1b[0m \x1b[1mINFO\x1b[0m Current multiprocessing start method"
)


class TokenizerTestCase(TestCase):
    def test_default(self):
        tokens = tokenize_ansi_escape_text(_TEST_ANSI_ESCAPE_TEXT)
        self.assertEqual(20, len(tokens))

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
        self.assertEqual(tokens[19].text, " Current multiprocessing start method")


if __name__ == "__main__":
    main()
