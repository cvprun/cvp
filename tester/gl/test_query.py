# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.gl.query import get_max_texture_size


class QueryTestCase(TestCase):
    def test_get_max_texture_size(self):
        self.assertIsInstance(get_max_texture_size(), int)


if __name__ == "__main__":
    main()
