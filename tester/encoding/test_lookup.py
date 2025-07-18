# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.encoding.lookup import BINARY_ENCODINGS, ENCODINGS, TEXT_ENCODINGS


class LookupTestCase(TestCase):
    def test_binary_encodings(self):
        self.assertLess(0, len(BINARY_ENCODINGS))
        self.assertIn("base64", BINARY_ENCODINGS)
        self.assertIn("zip", BINARY_ENCODINGS)
        self.assertIn("zlib", BINARY_ENCODINGS)
        self.assertIn("hex", BINARY_ENCODINGS)

    def test_text_encodings(self):
        self.assertLess(0, len(TEXT_ENCODINGS))
        self.assertIn("utf8", TEXT_ENCODINGS)
        self.assertIn("latin8", TEXT_ENCODINGS)

    def test_merged_encodings(self):
        merged_encodings = set(list(BINARY_ENCODINGS) + list(TEXT_ENCODINGS))
        self.assertSetEqual(set(ENCODINGS), merged_encodings)


if __name__ == "__main__":
    main()
