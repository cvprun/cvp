# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.maths.numeral.si_prefixes import GIGA, KILO, MEGA, TERA, format_si_prefix


class SiPrefixesTestCase(TestCase):
    def test_units(self):
        self.assertEqual(1000**1, KILO)
        self.assertEqual(1000**2, MEGA)
        self.assertEqual(1000**3, GIGA)
        self.assertEqual(1000**4, TERA)

    def test_none(self):
        self.assertEqual("0.000", format_si_prefix(0))
        self.assertEqual("1.000", format_si_prefix(1))
        self.assertEqual("20.000", format_si_prefix(20))
        self.assertEqual("999.000", format_si_prefix(999))

        self.assertEqual("0.00", format_si_prefix(0, precision=2))
        self.assertEqual("1.00", format_si_prefix(1, precision=2))
        self.assertEqual("20.00", format_si_prefix(20, precision=2))
        self.assertEqual("999.00", format_si_prefix(999, precision=2))

        self.assertEqual("0.0", format_si_prefix(0, precision=1))
        self.assertEqual("1.0", format_si_prefix(1, precision=1))
        self.assertEqual("20.0", format_si_prefix(20, precision=1))
        self.assertEqual("999.0", format_si_prefix(999, precision=1))

        self.assertEqual("0", format_si_prefix(0, precision=0))
        self.assertEqual("1", format_si_prefix(1, precision=0))
        self.assertEqual("20", format_si_prefix(20, precision=0))
        self.assertEqual("999", format_si_prefix(999, precision=0))

    def test_kilo(self):
        self.assertEqual("1.000k", format_si_prefix(KILO))
        self.assertEqual("999.999k", format_si_prefix(MEGA - 1))

        self.assertEqual("1.00k", format_si_prefix(KILO, precision=2))
        self.assertEqual("999.99k", format_si_prefix(MEGA - 1, precision=2))

        self.assertEqual("1.0k", format_si_prefix(KILO, precision=1))
        self.assertEqual("999.9k", format_si_prefix(MEGA - 1, precision=1))

        self.assertEqual("1k", format_si_prefix(KILO, precision=0))
        self.assertEqual("999k", format_si_prefix(MEGA - 1, precision=0))

    def test_mega(self):
        self.assertEqual("1.000M", format_si_prefix(MEGA))
        self.assertEqual("999.999M", format_si_prefix(GIGA - 1))

        self.assertEqual("1.00M", format_si_prefix(MEGA, precision=2))
        self.assertEqual("999.99M", format_si_prefix(GIGA - 1, precision=2))

        self.assertEqual("1.0M", format_si_prefix(MEGA, precision=1))
        self.assertEqual("999.9M", format_si_prefix(GIGA - 1, precision=1))

        self.assertEqual("1M", format_si_prefix(MEGA, precision=0))
        self.assertEqual("999M", format_si_prefix(GIGA - 1, precision=0))

    def test_giga(self):
        self.assertEqual("1.000G", format_si_prefix(GIGA))
        self.assertEqual("999.999G", format_si_prefix(TERA - 1))

        self.assertEqual("1.00G", format_si_prefix(GIGA, precision=2))
        self.assertEqual("999.99G", format_si_prefix(TERA - 1, precision=2))

        self.assertEqual("1.0G", format_si_prefix(GIGA, precision=1))
        self.assertEqual("999.9G", format_si_prefix(TERA - 1, precision=1))

        self.assertEqual("1G", format_si_prefix(GIGA, precision=0))
        self.assertEqual("999G", format_si_prefix(TERA - 1, precision=0))


if __name__ == "__main__":
    main()
