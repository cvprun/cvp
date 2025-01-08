# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.flow.catalog import FlowCatalog


class DefaultTestCase(TestCase):
    def test_default(self):
        catalog = FlowCatalog()
        self.assertTrue(bool(catalog))


if __name__ == "__main__":
    main()
