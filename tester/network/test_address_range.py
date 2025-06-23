# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.network.address_range import calc_ip_range, calc_ipv4_range, calc_ipv6_range


class AddressRangeTestCase(TestCase):
    def test_calc_ipv4_range(self):
        expect_ips = ["192.168.0.1", "192.168.0.2", "192.168.0.3", "192.168.0.4"]
        actual_ips = calc_ipv4_range("192.168.0.1", "192.168.0.4")
        self.assertEqual(expect_ips, actual_ips)

    def test_calc_ipv6_range(self):
        expect_ips = ["::1", "::2", "::3"]
        actual_ips = calc_ipv6_range("::1", "::3")
        self.assertEqual(expect_ips, actual_ips)

    def test_errors(self):
        with self.assertRaises(ValueError):
            calc_ip_range("192.168.0.1", "::3")


if __name__ == "__main__":
    main()
