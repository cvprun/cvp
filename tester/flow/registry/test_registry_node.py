# -*- coding: utf-8 -*-

from typing import Any
from unittest import TestCase, main

from cvp.flow.registry.registry import FlowRegistry


class RegistryNodeTestCase(TestCase):
    def test_register_nodes_builtins(self):
        registry = FlowRegistry(no_builtins=True)
        self.assertEqual(0, len(registry.dtypes))
        self.assertEqual(0, len(registry.type2dtypes))
        self.assertEqual(0, len(registry.nodes))

        registry.register_builtin_nodes()
        self.assertEqual(1, len(registry.dtypes))
        self.assertEqual(1, len(registry.type2dtypes))
        self.assertNotEqual(0, len(registry.nodes))

        self.assertEqual(Any, registry.get_dtype_with_type(Any).base)
        self.assertEqual(Any, registry.get_dtype("typing.Any").base)


if __name__ == "__main__":
    main()
