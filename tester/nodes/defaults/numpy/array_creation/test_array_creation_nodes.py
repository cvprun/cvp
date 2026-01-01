# -*- coding: utf-8 -*-

from unittest import TestCase

import numpy as np

from cvp.nodes.defaults.numpy.array_creation.arange_node import ArangeNode
from cvp.nodes.defaults.numpy.array_creation.array_node import ArrayNode
from cvp.nodes.defaults.numpy.array_creation.empty_node import EmptyNode
from cvp.nodes.defaults.numpy.array_creation.eye_node import EyeNode
from cvp.nodes.defaults.numpy.array_creation.full_node import FullNode
from cvp.nodes.defaults.numpy.array_creation.identity_node import IdentityNode
from cvp.nodes.defaults.numpy.array_creation.linspace_node import LinspaceNode
from cvp.nodes.defaults.numpy.array_creation.logspace_node import LogspaceNode
from cvp.nodes.defaults.numpy.array_creation.ones_node import OnesNode
from cvp.nodes.defaults.numpy.array_creation.zeros_node import ZerosNode
from cvp.nodes.record import NodeRecord


class TestArrayCreationNodes(TestCase):

    def setUp(self):
        self.record = NodeRecord.empty()

    def test_arange_node(self):
        """Test ArangeNode functionality."""
        node = ArangeNode()

        # Test basic arange with stop only (start=0, step=1 by default)
        self.record.set(node._input_pins[1], 5)  # stop pin
        node.run(self.record)
        result = self.record.get(node._output)
        np.testing.assert_array_equal(result, np.arange(0, 5, 1))

        # Test with start and stop
        self.record = NodeRecord.empty()
        self.record.set(node._input_pins[0], 2)  # start
        self.record.set(node._input_pins[1], 8)  # stop
        node.run(self.record)
        result = self.record.get(node._output)
        np.testing.assert_array_equal(result, np.arange(2, 8, 1))

    def test_array_node(self):
        """Test ArrayNode functionality."""
        node = ArrayNode()

        # Test with list input (object pin)
        test_data = [1, 2, 3, 4, 5]
        self.record.set(node._input_pins[0], test_data)  # object pin
        node.run(self.record)
        result = self.record.get(node._output)
        np.testing.assert_array_equal(result, np.array(test_data))

        # Test with nested list
        self.record = NodeRecord.empty()
        test_data = [[1, 2], [3, 4]]
        self.record.set(node._input_pins[0], test_data)  # object pin
        node.run(self.record)
        result = self.record.get(node._output)
        np.testing.assert_array_equal(result, np.array(test_data))

    def test_empty_node(self):
        """Test EmptyNode functionality."""
        node = EmptyNode()

        # Test creating empty array
        shape = (3, 4)
        self.record.set(node._input_pins[0], shape)
        node.run(self.record)
        result = self.record.get(node._output)
        self.assertEqual(result.shape, shape)
        self.assertEqual(result.dtype, float)

    def test_eye_node(self):
        """Test EyeNode functionality."""
        node = EyeNode()

        # Test identity matrix creation
        n = 3
        self.record.set(node._input_pins[0], n)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.eye(3)
        np.testing.assert_array_equal(result, expected)

    def test_full_node(self):
        """Test FullNode functionality."""
        node = FullNode()

        # Test creating array filled with specific value
        shape = (2, 3)
        fill_value = 7
        self.record.set(node._input_pins[0], shape)
        self.record.set(node._input_pins[1], fill_value)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.full(shape, fill_value)
        np.testing.assert_array_equal(result, expected)

    def test_identity_node(self):
        """Test IdentityNode functionality."""
        node = IdentityNode()

        # Test identity matrix creation
        n = 4
        self.record.set(node._input_pins[0], n)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.identity(4)
        np.testing.assert_array_equal(result, expected)

    def test_linspace_node(self):
        """Test LinspaceNode functionality."""
        node = LinspaceNode()

        # Test linear spacing
        start, stop, num = 0, 10, 5
        self.record.set(node._input_pins[0], start)
        self.record.set(node._input_pins[1], stop)
        self.record.set(node._input_pins[2], num)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.linspace(start, stop, num)
        np.testing.assert_array_almost_equal(result, expected)

    def test_logspace_node(self):
        """Test LogspaceNode functionality."""
        node = LogspaceNode()

        # Test logarithmic spacing
        start, stop, num = 1, 3, 5
        self.record.set(node._input_pins[0], start)
        self.record.set(node._input_pins[1], stop)
        self.record.set(node._input_pins[2], num)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.logspace(start, stop, num)
        np.testing.assert_array_almost_equal(result, expected)

    def test_ones_node(self):
        """Test OnesNode functionality."""
        node = OnesNode()

        # Test creating ones array
        shape = (2, 4)
        self.record.set(node._input_pins[0], shape)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.ones(shape)
        np.testing.assert_array_equal(result, expected)

    def test_zeros_node(self):
        """Test ZerosNode functionality."""
        node = ZerosNode()

        # Test creating zeros array
        shape = (3, 3)
        self.record.set(node._input_pins[0], shape)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.zeros(shape)
        np.testing.assert_array_equal(result, expected)

        # Test with different dtype
        self.record = NodeRecord.empty()
        self.record.set(node._input_pins[0], shape)
        self.record.set(node._input_pins[1], int)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.zeros(shape, dtype=int)
        np.testing.assert_array_equal(result, expected)
        self.assertEqual(result.dtype, int)