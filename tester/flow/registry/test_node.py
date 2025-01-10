# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.flow.registry.node import GlobalFlowNodeRegistry, global_node_registry


class DefaultTestCase(TestCase):
    def test_global(self):
        catalog = global_node_registry()
        catalog1 = GlobalFlowNodeRegistry()
        catalog2 = GlobalFlowNodeRegistry()
        self.assertEqual(catalog, catalog1)
        self.assertEqual(catalog, catalog2)


if __name__ == "__main__":
    main()
