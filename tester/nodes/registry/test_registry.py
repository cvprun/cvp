# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.nodes.registry.globals import GlobalNodeRegistry, global_node_registry
from cvp.nodes.registry.registry import NodeRegistry
from cvp.pins.special import NextPin, PrevPin, ReturnPin
from cvp.variables import FLOW_PATH_SEPARATOR


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

    def test_register_node_abs(self):
        registry = NodeRegistry(no_defaults=True)
        self.assertEqual(0, len(registry))

        registry.add_new(abs)
        self.assertEqual(1, len(registry))

        abs_node = registry.get("builtins.abs")
        self.assertEqual(abs, abs_node.func)
        self.assertEqual(10, abs_node(-10))

    def test_register_node_custom(self):
        registry = NodeRegistry(no_defaults=True)
        self.assertEqual(0, len(registry))

        @registry.register()
        def _add(a, b):
            return a + b

        self.assertEqual(1, len(registry))
        test_path = _add.__module__ + FLOW_PATH_SEPARATOR + _add.__name__
        self.assertEqual("tester.nodes.registry.test_registry._add", test_path)

        add_node = registry.get(test_path)
        self.assertEqual(_add, add_node.func)
        self.assertEqual(30, add_node(10, 20))

        any_dtype = registry.dtype_registry.any_dtype

        self.assertEqual(1, len(add_node.flow_inputs))
        self.assertEqual(1, len(add_node.flow_outputs))
        self.assertEqual(2, len(add_node.data_inputs))
        self.assertEqual(1, len(add_node.data_outputs))
        self.assertIsInstance(add_node.flow_inputs[0], PrevPin)
        self.assertIsInstance(add_node.flow_outputs[0], NextPin)
        self.assertEqual("a", add_node.data_inputs[0].name)
        self.assertEqual("b", add_node.data_inputs[1].name)
        self.assertEqual(any_dtype, add_node.data_inputs[0].dtype)
        self.assertEqual(any_dtype, add_node.data_inputs[1].dtype)
        self.assertIsInstance(add_node.data_outputs[0], ReturnPin)


if __name__ == "__main__":
    main()
