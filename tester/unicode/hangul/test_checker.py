# -*- coding: utf-8 -*-

from string import ascii_letters, digits, punctuation, whitespace
from unittest import TestCase, main

from cvp.unicode.hangul.checker import is_hangul_unicode


class CheckerTestCase(TestCase):
    def test_strings(self):
        self.assertTrue(all([not is_hangul_unicode(k) for k in digits]))
        self.assertTrue(all([not is_hangul_unicode(k) for k in punctuation]))
        self.assertTrue(all([not is_hangul_unicode(k) for k in ascii_letters]))
        self.assertTrue(all([not is_hangul_unicode(k) for k in whitespace]))


if __name__ == "__main__":
    main()
