# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.chrono.month_day import MonthDay, in_month_day


class MonthDayTestCase(TestCase):
    def test_from_format(self):
        self.assertTupleEqual((2, 9), MonthDay.from_format("02/09"))
        self.assertTupleEqual((12, 31), MonthDay.from_format("12/31"))

    def test_in_month_day(self):
        begin = MonthDay(4, 15)
        end = MonthDay(5, 19)

        self.assertTrue(in_month_day(MonthDay(4, 15), begin, end))
        self.assertTrue(in_month_day(MonthDay(5, 19), begin, end))

        self.assertTrue(in_month_day(MonthDay(4, 20), begin, end))
        self.assertTrue(in_month_day(MonthDay(5, 11), begin, end))

        self.assertFalse(in_month_day(MonthDay(4, 13), begin, end))
        self.assertFalse(in_month_day(MonthDay(3, 18), begin, end))
        self.assertFalse(in_month_day(MonthDay(5, 30), begin, end))
        self.assertFalse(in_month_day(MonthDay(6, 10), begin, end))

    def test_in_month_day_with_overflow(self):
        begin = MonthDay(10, 15)
        end = MonthDay(2, 19)

        self.assertTrue(in_month_day(MonthDay(10, 15), begin, end))
        self.assertTrue(in_month_day(MonthDay(2, 19), begin, end))

        self.assertTrue(in_month_day(MonthDay(10, 18), begin, end))
        self.assertTrue(in_month_day(MonthDay(11, 11), begin, end))
        self.assertTrue(in_month_day(MonthDay(12, 20), begin, end))

        self.assertTrue(in_month_day(MonthDay(1, 10), begin, end))
        self.assertTrue(in_month_day(MonthDay(2, 11), begin, end))

        self.assertFalse(in_month_day(MonthDay(10, 11), begin, end))
        self.assertFalse(in_month_day(MonthDay(2, 20), begin, end))
        self.assertFalse(in_month_day(MonthDay(4, 10), begin, end))


if __name__ == "__main__":
    main()
