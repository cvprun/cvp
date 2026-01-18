# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.sdp.models.bandwidth import Bandwidth


class BandwidthTestCase(TestCase):
    def test_encode(self) -> None:
        bw = Bandwidth(bwtype="AS", bandwidth=1000)
        self.assertEqual("b=AS:1000", bw.encode())

    def test_parse(self) -> None:
        bw = Bandwidth.parse("b=AS:2000")
        self.assertEqual("AS", bw.bwtype)
        self.assertEqual(2000, bw.bandwidth)

    def test_parse_ct(self) -> None:
        bw = Bandwidth.parse("b=CT:128")
        self.assertEqual("CT", bw.bwtype)
        self.assertEqual(128, bw.bandwidth)

    def test_parse_tias(self) -> None:
        bw = Bandwidth.parse("b=TIAS:500000")
        self.assertEqual("TIAS", bw.bwtype)
        self.assertEqual(500000, bw.bandwidth)

    def test_parse_invalid_prefix(self) -> None:
        with self.assertRaises(ValueError):
            Bandwidth.parse("invalid")

    def test_parse_invalid_format(self) -> None:
        with self.assertRaises(ValueError):
            Bandwidth.parse("b=AS")

    def test_str(self) -> None:
        bw = Bandwidth(bwtype="CT", bandwidth=256)
        self.assertEqual("b=CT:256", str(bw))


if __name__ == "__main__":
    main()
