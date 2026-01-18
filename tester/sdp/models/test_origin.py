# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.sdp.models.origin import Origin


class OriginTestCase(TestCase):
    def test_encode(self) -> None:
        origin = Origin(
            username="-",
            sess_id="123456",
            sess_version=2,
            nettype="IN",
            addrtype="IP4",
            unicast_address="127.0.0.1",
        )
        self.assertEqual("o=- 123456 2 IN IP4 127.0.0.1", origin.encode())

    def test_parse(self) -> None:
        origin = Origin.parse("o=- 123456 2 IN IP4 127.0.0.1")
        self.assertEqual("-", origin.username)
        self.assertEqual("123456", origin.sess_id)
        self.assertEqual(2, origin.sess_version)
        self.assertEqual("IN", origin.nettype)
        self.assertEqual("IP4", origin.addrtype)
        self.assertEqual("127.0.0.1", origin.unicast_address)

    def test_parse_invalid_prefix(self) -> None:
        with self.assertRaises(ValueError):
            Origin.parse("invalid")

    def test_parse_invalid_format(self) -> None:
        with self.assertRaises(ValueError):
            Origin.parse("o=- 123")

    def test_str(self) -> None:
        origin = Origin(
            username="alice",
            sess_id="1",
            sess_version=1,
            nettype="IN",
            addrtype="IP6",
            unicast_address="::1",
        )
        self.assertEqual("o=alice 1 1 IN IP6 ::1", str(origin))


if __name__ == "__main__":
    main()
