# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.network.uri.host_port import has_scheme


class HostPortTestCase(TestCase):
    def test_has_scheme(self):
        self.assertTrue(has_scheme("http://localhost/"))
        self.assertFalse(has_scheme("localhost:8080"))


if __name__ == "__main__":
    main()
