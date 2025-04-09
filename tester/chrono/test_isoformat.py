# -*- coding: utf-8 -*-

from datetime import UTC, datetime
from unittest import TestCase, main

from cvp.chrono.isoformat import (
    fromisoformat,
    fromisoformat_with_utc,
    isoformat,
    isoformat_with_utc,
)


class IsoformatTestCase(TestCase):
    def test_none_arguments(self):
        self.assertIsInstance(isoformat(), str)
        self.assertIsInstance(fromisoformat(), datetime)

        self.assertIsInstance(isoformat_with_utc(), str)
        self.assertIsInstance(fromisoformat_with_utc(), datetime)

    def test_utc(self):
        self.assertTrue(isoformat_with_utc().endswith("+00:00"))
        self.assertEqual(UTC, fromisoformat_with_utc().tzinfo)


if __name__ == "__main__":
    main()
