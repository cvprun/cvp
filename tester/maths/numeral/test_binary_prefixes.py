# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.maths.numeral.binary_prefixes import (
    BYTES_IN_GB,
    BYTES_IN_KB,
    BYTES_IN_MB,
    BYTES_IN_TB,
    format_binary_prefix,
)


class BinaryPrefixesTestCase(TestCase):
    def test_units(self):
        self.assertEqual(1024**1, BYTES_IN_KB)
        self.assertEqual(1024**2, BYTES_IN_MB)
        self.assertEqual(1024**3, BYTES_IN_GB)
        self.assertEqual(1024**4, BYTES_IN_TB)

    def test_none(self):
        self.assertEqual("0.00B", format_binary_prefix(0))
        self.assertEqual("1.00B", format_binary_prefix(1))
        self.assertEqual("20.00B", format_binary_prefix(20))
        self.assertEqual("999.00B", format_binary_prefix(999))
        self.assertEqual("1000.00B", format_binary_prefix(1000))
        self.assertEqual("1023.00B", format_binary_prefix(1023))

        self.assertEqual("0.0B", format_binary_prefix(0, precision=1))
        self.assertEqual("1.0B", format_binary_prefix(1, precision=1))
        self.assertEqual("20.0B", format_binary_prefix(20, precision=1))
        self.assertEqual("999.0B", format_binary_prefix(999, precision=1))
        self.assertEqual("1000.0B", format_binary_prefix(1000, precision=1))
        self.assertEqual("1023.0B", format_binary_prefix(1023, precision=1))

        self.assertEqual("0B", format_binary_prefix(0, precision=0))
        self.assertEqual("1B", format_binary_prefix(1, precision=0))
        self.assertEqual("20B", format_binary_prefix(20, precision=0))
        self.assertEqual("999B", format_binary_prefix(999, precision=0))
        self.assertEqual("1000B", format_binary_prefix(1000, precision=0))
        self.assertEqual("1023B", format_binary_prefix(1023, precision=0))

    def test_kilo(self):
        self.assertEqual("1.00KB", format_binary_prefix(BYTES_IN_KB))
        self.assertEqual("1023.99KB", format_binary_prefix(BYTES_IN_MB - 1))

        self.assertEqual("1.0KB", format_binary_prefix(BYTES_IN_KB, precision=1))
        self.assertEqual("1023.9KB", format_binary_prefix(BYTES_IN_MB - 1, precision=1))

        self.assertEqual("1KB", format_binary_prefix(BYTES_IN_KB, precision=0))
        self.assertEqual("1023KB", format_binary_prefix(BYTES_IN_MB - 1, precision=0))

    def test_mega(self):
        self.assertEqual("1.00MB", format_binary_prefix(BYTES_IN_MB))
        self.assertEqual("1023.99MB", format_binary_prefix(BYTES_IN_GB - 1))

        self.assertEqual("1.0MB", format_binary_prefix(BYTES_IN_MB, precision=1))
        self.assertEqual("1023.9MB", format_binary_prefix(BYTES_IN_GB - 1, precision=1))

        self.assertEqual("1MB", format_binary_prefix(BYTES_IN_MB, precision=0))
        self.assertEqual("1023MB", format_binary_prefix(BYTES_IN_GB - 1, precision=0))

    def test_giga(self):
        self.assertEqual("1.00GB", format_binary_prefix(BYTES_IN_GB))
        self.assertEqual("1023.99GB", format_binary_prefix(BYTES_IN_TB - 1))

        self.assertEqual("1.0GB", format_binary_prefix(BYTES_IN_GB, precision=1))
        self.assertEqual("1023.9GB", format_binary_prefix(BYTES_IN_TB - 1, precision=1))

        self.assertEqual("1GB", format_binary_prefix(BYTES_IN_GB, precision=0))
        self.assertEqual("1023GB", format_binary_prefix(BYTES_IN_TB - 1, precision=0))


if __name__ == "__main__":
    main()
