# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.maths.numeral.metric_prefix import calc_exponent


class MetricPrefixTestCase(TestCase):
    def test_calc_exponent_base2(self):
        self.assertEqual(10, calc_exponent(1024**1, 2))  # K
        self.assertEqual(20, calc_exponent(1024**2, 2))  # M
        self.assertEqual(30, calc_exponent(1024**3, 2))  # G
        self.assertEqual(40, calc_exponent(1024**4, 2))  # T
        self.assertEqual(50, calc_exponent(1024**5, 2))  # P
        self.assertEqual(60, calc_exponent(1024**6, 2))  # E
        self.assertEqual(70, calc_exponent(1024**7, 2))  # Z
        self.assertEqual(80, calc_exponent(1024**8, 2))  # Y
        self.assertEqual(90, calc_exponent(1024**9, 2))  # R
        self.assertEqual(100, calc_exponent(1024**10, 2))  # Q

    def test_calc_exponent_base10(self):
        self.assertEqual(3, calc_exponent(1000**1, 10))
        self.assertEqual(6, calc_exponent(1000**2, 10))
        self.assertEqual(9, calc_exponent(1000**3, 10))
        self.assertEqual(12, calc_exponent(1000**4, 10))
        self.assertEqual(15, calc_exponent(1000**5, 10))
        self.assertEqual(18, calc_exponent(1000**6, 10))
        self.assertEqual(21, calc_exponent(1000**7, 10))
        self.assertEqual(24, calc_exponent(1000**8, 10))
        self.assertEqual(27, calc_exponent(1000**9, 10))
        self.assertEqual(30, calc_exponent(1000**10, 10))

    def test_calc_exponent_base10_minus1(self):
        self.assertEqual(2, calc_exponent(1000**1 - 1, 10))
        self.assertEqual(5, calc_exponent(1000**2 - 1, 10))
        self.assertEqual(8, calc_exponent(1000**3 - 1, 10))
        self.assertEqual(11, calc_exponent(1000**4 - 1, 10))
        self.assertEqual(14, calc_exponent(1000**5 - 1, 10))
        self.assertEqual(17, calc_exponent(1000**6 - 1, 10))
        self.assertEqual(20, calc_exponent(1000**7 - 1, 10))
        self.assertEqual(23, calc_exponent(1000**8 - 1, 10))
        self.assertEqual(26, calc_exponent(1000**9 - 1, 10))
        self.assertEqual(29, calc_exponent(1000**10 - 1, 10))


if __name__ == "__main__":
    main()
