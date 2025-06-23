# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.network.host_port import parse_host_port


class HostPortTestCase(TestCase):
    def test_parse_host_port(self):
        self.assertTupleEqual(("[::1]", 8080), parse_host_port("[::1]:8080"))
        self.assertTupleEqual(("127.0.0.1", 8080), parse_host_port("127.0.0.1:8080"))


if __name__ == "__main__":
    main()
