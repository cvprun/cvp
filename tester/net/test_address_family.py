# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.net.address_family import is_ipv4_address, is_ipv6_address


class AddressFamilyTestCase(TestCase):
    def test_is_ipv4_address(self):
        self.assertTrue(is_ipv4_address("192.168.0.1"))

    def test_is_ipv6_address(self):
        self.assertTrue(is_ipv6_address("::1"))


if __name__ == "__main__":
    main()
