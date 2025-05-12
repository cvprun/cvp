# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.strings.parse_number_ranges import parse_integer_ranges


class ParseIntegerRangesTestCase(TestCase):
    def test_default(self):
        self.assertListEqual([80, 443], parse_integer_ranges("80,443"))
        self.assertListEqual([80, 81, 82], parse_integer_ranges("80-82"))
        self.assertListEqual([80, 443, 8, 9, 10], parse_integer_ranges("80,443,8-10"))


if __name__ == "__main__":
    main()
