# -*- coding: utf-8 -*-

from typing import Annotated, Optional, Union
from unittest import TestCase, main

from cvp.dtypes.dtype import Dtype
from cvp.nodes.callable import CallableNode
from cvp.nodes.node import Node
from cvp.nodes.registry.globals import GlobalNodeRegistry, global_node_registry
from cvp.nodes.registry.registry import NodeRegistry
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
            registry.add_callable(None)  # noqa

    def test_register_node_abs(self):
        registry = NodeRegistry(no_defaults=True)
        self.assertEqual(0, len(registry))

        registry.add_callable(abs)
        self.assertEqual(1, len(registry))

        abs_node = registry.get("builtins.abs")
        self.assertIsInstance(abs_node, CallableNode)

        self.assertEqual(10, abs_node(-10))

    def test_register_node_custom(self):
        registry = NodeRegistry(no_defaults=True)
        self.assertEqual(0, len(registry))

        @registry.register()
        def _add(a, b):
            return a + b

        self.assertEqual(1, len(registry))
        expect_path = "tester.nodes.registry.test_registry._add"
        actual_path = _add.__module__ + FLOW_PATH_SEPARATOR + _add.__name__
        self.assertEqual(expect_path, actual_path)

        add_node = registry.get(actual_path)
        self.assertEqual(30, add_node(10, 20))

    def test_register_node_custom_annotation_int(self):
        registry = NodeRegistry(no_defaults=True)

        @registry.register()
        def _add(a: int, b: int) -> int:
            return a + b

        self.assertEqual(1, len(registry))
        add_node = next(iter(registry.values()))
        pins = add_node.pins
        data_inputs = [pin for pin in pins if pin.is_data_inputs]
        data_outputs = [pin for pin in pins if pin.is_data_outputs]

        self.assertEqual(2, len(data_inputs))
        self.assertEqual(1, len(data_outputs))

        self.assertEqual(Dtype(int), data_inputs[0].dtype)
        self.assertEqual(Dtype(int), data_inputs[1].dtype)
        self.assertEqual(Dtype(int), data_outputs[0].dtype)

    def test_register_node_custom_annotation_union(self):
        registry = NodeRegistry(no_defaults=True)
        self.assertEqual(0, len(registry))

        with self.assertRaises(TypeError):

            @registry.register()
            def _add1(a: Union[int, float], b: Union[int, float]):
                return a + b

        with self.assertRaises(TypeError):

            @registry.register()
            def _add2(a, b) -> Union[int, float]:
                return a + b

        self.assertEqual(0, len(registry))

    def test_register_node_custom_annotation_optional(self):
        registry = NodeRegistry(no_defaults=True)
        self.assertEqual(0, len(registry))

        with self.assertRaises(TypeError):

            @registry.register()
            def _add1(a: Optional[int], b: Optional[int]):
                return a + b  # type: ignore[operator]

        with self.assertRaises(TypeError):

            @registry.register()
            def _add2(a, b) -> Optional[int]:
                return a + b

        self.assertEqual(0, len(registry))

    def test_register_node_custom_annotated(self):
        registry = NodeRegistry(no_defaults=True)
        self.assertEqual(0, len(registry))

        @registry.register()
        def _pow(a: Annotated[int, "base"]) -> Annotated[int, "result"]:
            return pow(a, 2)

        self.assertEqual(1, len(registry))

        node = next(iter(registry.values()))
        self.assertIsInstance(node, Node)
        pins = node.pins
        data_inputs = list(filter(lambda p: p.is_data_inputs, pins))
        data_outputs = list(filter(lambda p: p.is_data_outputs, pins))

        self.assertEqual(Dtype(int), data_inputs[0].dtype)
        self.assertEqual(Dtype(int), data_outputs[0].dtype)


if __name__ == "__main__":
    main()
