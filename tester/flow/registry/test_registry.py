# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.flow.registry.globals import FlowRegistry, GlobalFlowRegistry, global_registry


class RegistryTestCase(TestCase):
    def test_global(self):
        registry0 = global_registry()
        registry1 = GlobalFlowRegistry()
        registry2 = GlobalFlowRegistry()
        self.assertEqual(registry0, registry1)
        self.assertEqual(registry0, registry2)

    def test_empty_register_dtype(self):
        registry = FlowRegistry(no_builtins=True, no_defaults=True)
        self.assertEqual(0, len(registry.dtypes))
        self.assertEqual(0, len(registry.type2dtypes))
        self.assertEqual(0, len(registry.nodes))


if __name__ == "__main__":
    main()
