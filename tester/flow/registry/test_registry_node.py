# -*- coding: utf-8 -*-

from typing import Any
from unittest import TestCase, main

from cvp.flow.registry.registry import FlowRegistry


class RegistryNodeTestCase(TestCase):
    def test_register_nodes_builtins(self):
        registry = FlowRegistry(no_builtins=True, no_defaults=True)
        self.assertEqual(0, len(registry.dtypes))
        self.assertEqual(0, len(registry.type2dtypes))
        self.assertEqual(0, len(registry.nodes))

        registry.register_builtin_nodes()
        self.assertEqual(1, len(registry.dtypes))
        self.assertEqual(1, len(registry.type2dtypes))
        self.assertNotEqual(0, len(registry.nodes))

        self.assertEqual(Any, registry.get_dtype_with_type(Any).base)
        self.assertEqual(Any, registry.get_dtype("typing.Any").base)

    def test_register_node_error(self):
        registry = FlowRegistry(no_builtins=True, no_defaults=True)
        with self.assertRaises(TypeError):
            registry.add_new_callable(None)  # noqa

    def test_register_node_abs(self):
        registry = FlowRegistry(no_builtins=True, no_defaults=True)
        registry.add_new_callable(abs)

        self.assertEqual(1, len(registry.dtypes))
        self.assertEqual(1, len(registry.type2dtypes))
        self.assertEqual(1, len(registry.nodes))

        self.assertEqual(Any, registry.get_dtype_with_type(Any).base)
        self.assertEqual(Any, registry.get_dtype("typing.Any").base)

        abs_node = registry.get_node("builtins.abs")
        self.assertEqual(abs, abs_node.func)
        self.assertEqual(10, abs_node(-10))


if __name__ == "__main__":
    main()
