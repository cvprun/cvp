# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.gl.version import get_version, parse_version


class QueryTestCase(TestCase):
    def test_version(self):
        self.assertIsInstance(get_version(), str)

    def test_parse_version(self):
        sample = "4.6 (Compatibility Profile) Mesa 23.2.1"
        version = parse_version(sample)
        self.assertEqual(4, version[0])
        self.assertEqual(6, version[1])
        self.assertEqual("(Compatibility Profile) Mesa 23.2.1", version[2])


if __name__ == "__main__":
    main()
