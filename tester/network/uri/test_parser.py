# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.network.uri.parser import replace_netloc


class ParserTestCase(TestCase):
    def test_replace_netloc_1(self):
        src = "https://localhost:9999/download/index.html?latest#top"
        new = "http://www.onvif.org/ver10/schema"
        result = replace_netloc(src, new)
        self.assertEqual("https://www.onvif.org/download/index.html?latest#top", result)

    def test_replace_netloc_2(self):
        src = "http://localhost:9999/download"
        new = "https://www.onvif.org:8888/ver10/schema?latest#top"
        result = replace_netloc(src, new)
        self.assertEqual("http://www.onvif.org:8888/download", result)

    def test_replace_netloc_3(self):
        src = "http://localhost"
        new = "http://192.168.0.1:8080"
        result = replace_netloc(src, new)
        self.assertEqual("http://192.168.0.1:8080", result)

    def test_replace_netloc_4(self):
        src = "http://localhost?query=1&io=test"
        new = "http://192.168.0.44:22/"
        result = replace_netloc(src, new)
        self.assertEqual("http://192.168.0.44:22?query=1&io=test", result)

    def test_replace_netloc_5(self):
        src = "http://127.0.0.1:8080#latest"
        new = "http://localhost/?query=2"
        result = replace_netloc(src, new)
        self.assertEqual("http://localhost#latest", result)


if __name__ == "__main__":
    main()
