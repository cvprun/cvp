# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.sdp.models.timing import Timing


class TimingTestCase(TestCase):
    def test_encode(self) -> None:
        timing = Timing(start_time=0, stop_time=0)
        self.assertEqual("t=0 0", timing.encode())

    def test_parse(self) -> None:
        timing = Timing.parse("t=0 0")
        self.assertEqual(0, timing.start_time)
        self.assertEqual(0, timing.stop_time)

    def test_parse_with_values(self) -> None:
        timing = Timing.parse("t=3034423619 3042462419")
        self.assertEqual(3034423619, timing.start_time)
        self.assertEqual(3042462419, timing.stop_time)

    def test_parse_invalid_prefix(self) -> None:
        with self.assertRaises(ValueError):
            Timing.parse("invalid")

    def test_parse_invalid_format(self) -> None:
        with self.assertRaises(ValueError):
            Timing.parse("t=0")

    def test_str(self) -> None:
        timing = Timing(start_time=100, stop_time=200)
        self.assertEqual("t=100 200", str(timing))


if __name__ == "__main__":
    main()
