# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.maths.numeral.binary_prefixes import (
    BINARY_PREFIXES,
    binary_prefix_with_integer,
)


class SiPrefixesTestCase(TestCase):
    def test_none(self):
        no_prefix = BINARY_PREFIXES[0]
        self.assertTupleEqual((0, no_prefix), binary_prefix_with_integer(0))
        self.assertTupleEqual((1, no_prefix), binary_prefix_with_integer(1))
        self.assertTupleEqual((20, no_prefix), binary_prefix_with_integer(20))
        self.assertTupleEqual((999, no_prefix), binary_prefix_with_integer(999))
        self.assertTupleEqual((1000, no_prefix), binary_prefix_with_integer(1000))
        self.assertTupleEqual((1023, no_prefix), binary_prefix_with_integer(1023))

    def test_kilo(self):
        kilo = BINARY_PREFIXES[10]
        self.assertTupleEqual((1, kilo), binary_prefix_with_integer(1024))
        self.assertTupleEqual((1023, kilo), binary_prefix_with_integer(1024 * 1024 - 1))

    def test_mega(self):
        mega = BINARY_PREFIXES[20]
        self.assertTupleEqual((1, mega), binary_prefix_with_integer(1024 * 1024))
        self.assertTupleEqual(
            (1023, mega),
            binary_prefix_with_integer(1024 * 1024 * 1024 - 1),
        )

    def test_giga(self):
        giga = BINARY_PREFIXES[30]
        self.assertTupleEqual((1, giga), binary_prefix_with_integer(1024 * 1024 * 1024))
        self.assertTupleEqual(
            (1023, giga),
            binary_prefix_with_integer(1024 * 1024 * 1024 * 1024 - 1),
        )


if __name__ == "__main__":
    main()
