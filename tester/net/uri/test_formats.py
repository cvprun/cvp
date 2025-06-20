# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.net.uri.formats import format_path


class FormatsTestCase(TestCase):
    def test_format_path(self):
        actual1 = format_path("/api/{id}/info", dict(id=123))
        expect1 = "/api/123/info"
        self.assertEqual(expect1, actual1)

        actual2 = format_path("/api/{id}/info", dict(id=123), dict(limit=10, offset=0))
        expect2 = "/api/123/info?limit=10&offset=0"
        self.assertEqual(expect2, actual2)

        actual3 = format_path("/api/", queries={"a@b": "?"})
        expect3 = "/api/?a%40b=%3F"
        self.assertEqual(expect3, actual3)

        actual4 = format_path("/api test/")
        expect4 = "/api%20test/"
        self.assertEqual(expect4, actual4)

        actual4 = format_path("/api", queries={"aaa": None})
        expect4 = "/api"
        self.assertEqual(expect4, actual4)


if __name__ == "__main__":
    main()
