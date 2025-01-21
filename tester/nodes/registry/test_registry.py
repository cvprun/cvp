# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.nodes.registry.globals import GlobalNodeRegistry, global_node_registry
from cvp.nodes.registry.registry import NodeRegistry


class RegistryTestCase(TestCase):
    def test_global(self):
        registry0 = global_node_registry()
        registry1 = GlobalNodeRegistry()
        registry2 = GlobalNodeRegistry()
        self.assertEqual(registry0, registry1)
        self.assertEqual(registry0, registry2)

    def test_empty_register_node(self):
        registry = NodeRegistry(no_defaults=True)
        self.assertEqual(0, len(registry))

    def test_default_register_node(self):
        registry = NodeRegistry()
        self.assertNotEqual(0, len(registry))

    def test_register_node_error(self):
        registry = NodeRegistry(no_defaults=True)
        with self.assertRaises(TypeError):
            registry.add_new(None)  # noqa


if __name__ == "__main__":
    main()
