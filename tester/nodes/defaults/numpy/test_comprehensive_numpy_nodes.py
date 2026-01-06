# -*- coding: utf-8 -*-

import warnings
from unittest import TestCase, main

import numpy as np

from cvp.nodes.defaults.numpy import get_numpy_nodes
from cvp.nodes.defaults.numpy.array_creation.arange_node import ArangeNode
from cvp.nodes.defaults.numpy.array_creation.array_node import ArrayNode
from cvp.nodes.defaults.numpy.array_creation.ones_node import OnesNode
from cvp.nodes.defaults.numpy.array_creation.zeros_node import ZerosNode
from cvp.nodes.defaults.numpy.array_manipulation.reshape_node import ReshapeNode
from cvp.nodes.defaults.numpy.fft.fft_node import FftNode
from cvp.nodes.defaults.numpy.linalg.dot_node import DotNode
from cvp.nodes.defaults.numpy.logic.equal_node import EqualNode
from cvp.nodes.defaults.numpy.mathematical.add_node import AddNode
from cvp.nodes.defaults.numpy.mathematical.cos_node import CosNode
from cvp.nodes.defaults.numpy.mathematical.sin_node import SinNode
from cvp.nodes.defaults.numpy.mathematical.sqrt_node import SqrtNode
from cvp.nodes.defaults.numpy.random.random_random_node import RandomRandomNode
from cvp.nodes.defaults.numpy.statistics.mean_node import MeanNode
from cvp.nodes.defaults.numpy.statistics.sum_node import SumNode
from cvp.nodes.record import NodeRecord


class ComprehensiveNumpyNodesTestCase(TestCase):
    """Comprehensive tests for all numpy nodes."""

    def setUp(self):
        self.record = NodeRecord.empty()
        # Suppress warnings for tests
        warnings.filterwarnings("ignore")

    def test_all_numpy_nodes_instantiation(self):
        """Test that all numpy nodes can be instantiated without errors."""
        nodes = get_numpy_nodes()
        self.assertIsInstance(nodes, list)
        self.assertGreater(len(nodes), 150)

        failed_nodes = []
        for node_class in nodes:
            try:
                instance = node_class()
                self.assertTrue(hasattr(instance, "_input_pins"))
                self.assertTrue(hasattr(instance, "_output"))
            except Exception as e:
                failed_nodes.append((node_class.__class__.__name__, str(e)))

        if failed_nodes:
            self.fail(f"Failed to instantiate nodes: {failed_nodes}")

    # Array Creation Tests
    def test_array_creation_nodes(self):
        """Test array creation nodes."""
        # Test ArrayNode
        array_node = ArrayNode()
        test_data = [1, 2, 3, 4, 5]
        self.record.set(array_node._input_pins[0], test_data)
        array_node.run(self.record)
        result = self.record.get(array_node._output)
        np.testing.assert_array_equal(result, np.array(test_data))

        # Test ZerosNode
        self.record = NodeRecord.empty()
        zeros_node = ZerosNode()
        shape = (2, 3)
        self.record.set(zeros_node._input_pins[0], shape)
        zeros_node.run(self.record)
        result = self.record.get(zeros_node._output)
        expected = np.zeros(shape)
        np.testing.assert_array_equal(result, expected)

        # Test OnesNode
        self.record = NodeRecord.empty()
        ones_node = OnesNode()
        shape = (3, 2)
        self.record.set(ones_node._input_pins[0], shape)
        ones_node.run(self.record)
        result = self.record.get(ones_node._output)
        expected = np.ones(shape)
        np.testing.assert_array_equal(result, expected)

        # Test ArangeNode
        self.record = NodeRecord.empty()
        arange_node = ArangeNode()
        self.record.set(arange_node._input_pins[1], 5)  # stop
        arange_node.run(self.record)
        result = self.record.get(arange_node._output)
        expected = np.arange(0, 5, 1)  # start=0, step=1 by default
        np.testing.assert_array_equal(result, expected)

    # Mathematical Operations Tests
    def test_mathematical_nodes(self):
        """Test mathematical operation nodes."""
        # Test trigonometric functions
        sin_node = SinNode()
        self.record.set(sin_node._input_pins[0], np.pi / 2)
        sin_node.run(self.record)
        result = self.record.get(sin_node._output)
        np.testing.assert_almost_equal(result, 1.0, decimal=5)

        self.record = NodeRecord.empty()
        cos_node = CosNode()
        self.record.set(cos_node._input_pins[0], 0)
        cos_node.run(self.record)
        result = self.record.get(cos_node._output)
        np.testing.assert_almost_equal(result, 1.0, decimal=5)

        # Test arithmetic operations
        self.record = NodeRecord.empty()
        add_node = AddNode()
        arr1 = np.array([1, 2, 3])
        arr2 = np.array([4, 5, 6])
        self.record.set(add_node._input_pins[0], arr1)
        self.record.set(add_node._input_pins[1], arr2)
        add_node.run(self.record)
        result = self.record.get(add_node._output)
        expected = np.array([5, 7, 9])
        np.testing.assert_array_equal(result, expected)

        # Test sqrt
        self.record = NodeRecord.empty()
        sqrt_node = SqrtNode()
        self.record.set(sqrt_node._input_pins[0], 16)
        sqrt_node.run(self.record)
        result = self.record.get(sqrt_node._output)
        np.testing.assert_almost_equal(result, 4.0, decimal=5)

    # Array Manipulation Tests
    def test_array_manipulation_nodes(self):
        """Test array manipulation nodes."""
        # Test ReshapeNode
        reshape_node = ReshapeNode()
        arr = np.array([1, 2, 3, 4, 5, 6])
        new_shape = (2, 3)
        self.record.set(reshape_node._input_pins[0], arr)
        self.record.set(reshape_node._input_pins[1], new_shape)
        reshape_node.run(self.record)
        result = self.record.get(reshape_node._output)
        expected = arr.reshape(new_shape)
        np.testing.assert_array_equal(result, expected)

    # Statistics Tests
    def test_statistics_nodes(self):
        """Test statistics nodes."""
        test_array = np.array([1, 2, 3, 4, 5])

        # Test MeanNode
        mean_node = MeanNode()
        self.record.set(mean_node._input_pins[0], test_array)
        mean_node.run(self.record)
        result = self.record.get(mean_node._output)
        expected = np.mean(test_array)
        np.testing.assert_almost_equal(result, expected)

        # Test SumNode
        self.record = NodeRecord.empty()
        sum_node = SumNode()
        self.record.set(sum_node._input_pins[0], test_array)
        sum_node.run(self.record)
        result = self.record.get(sum_node._output)
        expected = np.sum(test_array)
        np.testing.assert_equal(result, expected)

    # Linear Algebra Tests
    def test_linalg_nodes(self):
        """Test linear algebra nodes."""
        # Test DotNode
        dot_node = DotNode()
        vec1 = np.array([1, 2, 3])
        vec2 = np.array([4, 5, 6])
        self.record.set(dot_node._input_pins[0], vec1)
        self.record.set(dot_node._input_pins[1], vec2)
        dot_node.run(self.record)
        result = self.record.get(dot_node._output)
        expected = np.dot(vec1, vec2)
        np.testing.assert_almost_equal(result, expected)

    # Logic Tests
    def test_logic_nodes(self):
        """Test logic nodes."""
        # Test EqualNode
        equal_node = EqualNode()
        arr1 = np.array([1, 2, 3])
        arr2 = np.array([1, 3, 3])
        self.record.set(equal_node._input_pins[0], arr1)
        self.record.set(equal_node._input_pins[1], arr2)
        equal_node.run(self.record)
        result = self.record.get(equal_node._output)
        expected = np.equal(arr1, arr2)
        np.testing.assert_array_equal(result, expected)

    # Random Tests
    def test_random_nodes(self):
        """Test random nodes."""
        # Test RandomRandomNode
        random_node = RandomRandomNode()
        size = (2, 3)
        self.record.set(random_node._input_pins[0], size)
        random_node.run(self.record)
        result = self.record.get(random_node._output)
        self.assertEqual(result.shape, size)
        self.assertTrue(np.all((result >= 0) & (result < 1)))

    # FFT Tests
    def test_fft_nodes(self):
        """Test FFT nodes."""
        # Test FftNode
        fft_node = FftNode()
        test_signal = np.array([1, 2, 3, 4])
        self.record.set(fft_node._input_pins[0], test_signal)
        fft_node.run(self.record)
        result = self.record.get(fft_node._output)
        expected = np.fft.fft(test_signal)
        np.testing.assert_array_almost_equal(result, expected)

    def test_node_inheritance_and_structure(self):
        """Test that nodes have proper inheritance and structure."""
        from cvp.nodes.defaults.numpy._base import NumpyFunctionNode

        # Test a few representative nodes
        sin_node = SinNode()
        add_node = AddNode()
        array_node = ArrayNode()

        # Check inheritance
        self.assertIsInstance(sin_node, NumpyFunctionNode)
        self.assertIsInstance(add_node, NumpyFunctionNode)
        self.assertIsInstance(array_node, NumpyFunctionNode)

        # Check structure
        for node in [sin_node, add_node, array_node]:
            self.assertTrue(hasattr(node, "_input_pins"))
            self.assertTrue(hasattr(node, "_output"))
            self.assertGreater(len(node._input_pins), 0)

            # Check pin properties
            for pin in node._input_pins:
                self.assertTrue(hasattr(pin, "name"))
                self.assertTrue(hasattr(pin, "dtype"))

            output_pin = node._output
            self.assertTrue(hasattr(output_pin, "name"))
            self.assertTrue(hasattr(output_pin, "dtype"))

    def test_error_handling(self):
        """Test error handling in nodes."""
        # Test with invalid inputs where appropriate
        sqrt_node = SqrtNode()

        # Test with negative number (should work but may produce warning)
        try:
            self.record.set(sqrt_node._input_pins[0], -1)
            sqrt_node.run(self.record)
            result = self.record.get(sqrt_node._output)
            # Should produce NaN for negative input
            self.assertTrue(np.isnan(result))
        except (ValueError, RuntimeWarning):
            # It's acceptable if this raises an error or warning
            pass

    def test_data_type_preservation(self):
        """Test that nodes preserve or handle data types correctly."""
        # Test with different data types
        sin_node = SinNode()

        # Test with float32
        self.record = NodeRecord.empty()
        input_val = np.float32(0.5)
        self.record.set(sin_node._input_pins[0], input_val)
        sin_node.run(self.record)
        result = self.record.get(sin_node._output)
        expected = np.sin(input_val)
        np.testing.assert_almost_equal(result, expected)

        # Test with complex numbers
        self.record = NodeRecord.empty()
        complex_val = 1 + 2j
        self.record.set(sin_node._input_pins[0], complex_val)
        sin_node.run(self.record)
        result = self.record.get(sin_node._output)
        expected = np.sin(complex_val)
        np.testing.assert_almost_equal(result, expected)

    def test_array_broadcasting(self):
        """Test that nodes handle array broadcasting correctly."""
        add_node = AddNode()

        # Test broadcasting scalar with array
        scalar = 5
        array = np.array([1, 2, 3])
        self.record.set(add_node._input_pins[0], scalar)
        self.record.set(add_node._input_pins[1], array)
        add_node.run(self.record)
        result = self.record.get(add_node._output)
        expected = scalar + array
        np.testing.assert_array_equal(result, expected)

        # Test broadcasting arrays of different shapes
        self.record = NodeRecord.empty()
        arr1 = np.array([[1], [2], [3]])  # (3, 1)
        arr2 = np.array([1, 2])  # (2,)
        self.record.set(add_node._input_pins[0], arr1)
        self.record.set(add_node._input_pins[1], arr2)
        add_node.run(self.record)
        result = self.record.get(add_node._output)
        expected = arr1 + arr2
        np.testing.assert_array_equal(result, expected)


if __name__ == "__main__":
    main()
