# -*- coding: utf-8 -*-

from unittest import TestCase, main

import numpy as np

from cvp.nodes.defaults.numpy import get_numpy_nodes
from cvp.nodes.defaults.numpy.mathematical.add_node import AddNode
from cvp.nodes.defaults.numpy.mathematical.cos_node import CosNode
from cvp.nodes.defaults.numpy.mathematical.sin_node import SinNode
from cvp.nodes.record import NodeRecord


class NumpyNodesTestCase(TestCase):
    def test_get_numpy_nodes(self):
        """Test that get_numpy_nodes returns a list of nodes."""
        nodes = get_numpy_nodes()
        self.assertIsInstance(nodes, list)
        self.assertGreater(len(nodes), 150)  # Should have 182 nodes

    def test_sin_node(self):
        """Test SinNode functionality."""
        sin_node = SinNode()
        record = NodeRecord.empty()

        # Test with scalar input
        test_input = np.pi / 2
        record.set(sin_node._input_pins[0], test_input)
        sin_node.run(record)
        result = record.get(sin_node._output)

        np.testing.assert_almost_equal(result, 1.0, decimal=5)

    def test_cos_node(self):
        """Test CosNode functionality."""
        cos_node = CosNode()
        record = NodeRecord.empty()

        # Test with scalar input
        test_input = 0
        record.set(cos_node._input_pins[0], test_input)
        cos_node.run(record)
        result = record.get(cos_node._output)

        np.testing.assert_almost_equal(result, 1.0, decimal=5)

    def test_add_node(self):
        """Test AddNode functionality."""
        add_node = AddNode()
        record = NodeRecord.empty()

        # Test with array inputs
        test_input1 = np.array([1, 2, 3])
        test_input2 = np.array([4, 5, 6])
        record.set(add_node._input_pins[0], test_input1)
        record.set(add_node._input_pins[1], test_input2)
        add_node.run(record)
        result = record.get(add_node._output)

        expected = np.array([5, 7, 9])
        np.testing.assert_array_equal(result, expected)

    def test_node_inheritance(self):
        """Test that all numpy nodes inherit from proper base classes."""
        from cvp.nodes.defaults.numpy._base import NumpyFunctionNode

        sin_node = SinNode()
        self.assertIsInstance(sin_node, NumpyFunctionNode)

        add_node = AddNode()
        self.assertIsInstance(add_node, NumpyFunctionNode)

    def test_node_pins(self):
        """Test that nodes have proper pin configuration."""
        sin_node = SinNode()

        # Check that node has input and output pins
        self.assertTrue(hasattr(sin_node, "_input_pins"))
        self.assertTrue(hasattr(sin_node, "_output"))
        self.assertGreater(len(sin_node._input_pins), 0)

        # Check pin properties
        input_pin = sin_node._input_pins[0]
        output_pin = sin_node._output

        self.assertTrue(hasattr(input_pin, "name"))
        self.assertTrue(hasattr(input_pin, "dtype"))
        self.assertTrue(hasattr(output_pin, "name"))
        self.assertTrue(hasattr(output_pin, "dtype"))


if __name__ == "__main__":
    main()
