# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.sdp.models.connection import Connection


class ConnectionTestCase(TestCase):
    def test_encode(self) -> None:
        conn = Connection(
            nettype="IN",
            addrtype="IP4",
            connection_address="0.0.0.0",
        )
        self.assertEqual("c=IN IP4 0.0.0.0", conn.encode())

    def test_parse(self) -> None:
        conn = Connection.parse("c=IN IP4 192.168.1.1")
        self.assertEqual("IN", conn.nettype)
        self.assertEqual("IP4", conn.addrtype)
        self.assertEqual("192.168.1.1", conn.connection_address)

    def test_parse_ipv6(self) -> None:
        conn = Connection.parse("c=IN IP6 ::1")
        self.assertEqual("IN", conn.nettype)
        self.assertEqual("IP6", conn.addrtype)
        self.assertEqual("::1", conn.connection_address)

    def test_parse_invalid_prefix(self) -> None:
        with self.assertRaises(ValueError):
            Connection.parse("invalid")

    def test_parse_invalid_format(self) -> None:
        with self.assertRaises(ValueError):
            Connection.parse("c=IN IP4")

    def test_str(self) -> None:
        conn = Connection(
            nettype="IN",
            addrtype="IP4",
            connection_address="10.0.0.1",
        )
        self.assertEqual("c=IN IP4 10.0.0.1", str(conn))


if __name__ == "__main__":
    main()
