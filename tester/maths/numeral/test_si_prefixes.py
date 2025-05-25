# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.maths.numeral.si_prefixes import SI_PREFIXES, si_prefix_with_integer


class SiPrefixesTestCase(TestCase):
    def test_none(self):
        no_prefix = SI_PREFIXES[0]
        self.assertTupleEqual((0, no_prefix), si_prefix_with_integer(0))
        self.assertTupleEqual((1, no_prefix), si_prefix_with_integer(1))
        self.assertTupleEqual((20, no_prefix), si_prefix_with_integer(20))
        self.assertTupleEqual((999, no_prefix), si_prefix_with_integer(999))

    def test_kilo(self):
        kilo = SI_PREFIXES[3]
        self.assertTupleEqual((1, kilo), si_prefix_with_integer(1_000))
        self.assertTupleEqual((999, kilo), si_prefix_with_integer(999_999))

    def test_mega(self):
        mega = SI_PREFIXES[6]
        self.assertTupleEqual((1, mega), si_prefix_with_integer(1_000_000))
        self.assertTupleEqual((999, mega), si_prefix_with_integer(999_999_999))

    def test_giga(self):
        giga = SI_PREFIXES[9]
        self.assertTupleEqual((1, giga), si_prefix_with_integer(1_000_000_000))
        self.assertTupleEqual((999, giga), si_prefix_with_integer(999_999_999_999))


if __name__ == "__main__":
    main()
