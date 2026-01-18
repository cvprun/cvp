# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.sdp.models.attribute import Attribute


class AttributeTestCase(TestCase):
    def test_encode_with_value(self) -> None:
        attr = Attribute(name="mid", value="0")
        self.assertEqual("a=mid:0", attr.encode())

    def test_encode_without_value(self) -> None:
        attr = Attribute(name="sendrecv")
        self.assertEqual("a=sendrecv", attr.encode())

    def test_parse_with_value(self) -> None:
        attr = Attribute.parse("a=mid:0")
        self.assertEqual("mid", attr.name)
        self.assertEqual("0", attr.value)

    def test_parse_without_value(self) -> None:
        attr = Attribute.parse("a=sendrecv")
        self.assertEqual("sendrecv", attr.name)
        self.assertIsNone(attr.value)

    def test_parse_with_colon_in_value(self) -> None:
        attr = Attribute.parse("a=fingerprint:sha-256 AB:CD:EF")
        self.assertEqual("fingerprint", attr.name)
        self.assertEqual("sha-256 AB:CD:EF", attr.value)

    def test_parse_invalid(self) -> None:
        with self.assertRaises(ValueError):
            Attribute.parse("invalid")

    def test_str(self) -> None:
        attr = Attribute(name="rtcp-mux")
        self.assertEqual("a=rtcp-mux", str(attr))


if __name__ == "__main__":
    main()
