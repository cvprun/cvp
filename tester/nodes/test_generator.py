# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.nodes.callable import CallableNode
from cvp.nodes.generator import generate_node
from cvp.nodes.node import Node
from cvp.nodes.ntype import Ntype
from cvp.nodes.record import NodeRecord
from cvp.pins.pin import Pin
from cvp.pins.special import EmptyNextPin
from cvp.types.override import override


class _TestNodeInterface(Node):
    @override
    def run(self, record: NodeRecord) -> Pin:
        return EmptyNextPin()

    @override
    def render(self, record: NodeRecord) -> None:
        pass


def _test_callable_func(x: int, y: int) -> int:
    return x + y


class GeneratorTestCase(TestCase):
    def test_generate_node_from_node_interface(self):
        ntype = Ntype(_TestNodeInterface)
        self.assertTrue(ntype.is_node_interface())

        node = generate_node(ntype)

        self.assertIsInstance(node, Node)
        self.assertIsInstance(node, _TestNodeInterface)
        self.assertNotIsInstance(node, CallableNode)

    def test_generate_node_from_callable(self):
        ntype = Ntype(_test_callable_func)
        self.assertTrue(ntype.is_callable())
        self.assertFalse(ntype.is_node_interface())

        node = generate_node(ntype)

        self.assertIsInstance(node, Node)
        self.assertIsInstance(node, CallableNode)

    def test_generate_node_callable_execution(self):
        ntype = Ntype(_test_callable_func)
        node = generate_node(ntype)

        self.assertIsInstance(node, CallableNode)
        result = node(3, 4)
        self.assertEqual(result, 7)

    def test_generate_node_from_builtin(self):
        ntype = Ntype(abs)
        node = generate_node(ntype)

        self.assertIsInstance(node, CallableNode)
        result = node(-5)
        self.assertEqual(result, 5)


if __name__ == "__main__":
    main()
