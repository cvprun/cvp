# -*- coding: utf-8 -*-

from unittest import TestCase, main
from zoneinfo import ZoneInfo

from cvp.chrono.timezones import UTC_OFFSETS, format_utc_offset


class TimezonesTestCase(TestCase):
    def test_format_utc_offset(self):
        self.assertEqual("+09:00", format_utc_offset(ZoneInfo("Asia/Seoul")))
        self.assertEqual("+09:00", UTC_OFFSETS["Asia/Seoul"])


if __name__ == "__main__":
    main()
