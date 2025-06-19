# -*- coding: utf-8 -*-

from unittest import TestCase, main

from pydantic import HttpUrl

from cvp.mediamtx.model import load_mediamtx_model


class ModelTestCase(TestCase):
    def test_default(self):
        model = load_mediamtx_model()
        self.assertEqual("3.0.0", model.openapi)
        self.assertEqual("1.0.0", model.info.version)
        self.assertEqual("MediaMTX API", model.info.title)
        self.assertEqual("MIT", model.info.license.name)
        self.assertEqual(HttpUrl("http://localhost:9997"), model.servers[0].url)
        self.assertEqual(0, len(model.security))


if __name__ == "__main__":
    main()
