# -*- coding: utf-8 -*-

from unittest import TestCase, main
import warnings

import numpy as np

from cvp.nodes.defaults.numpy import get_numpy_nodes
from cvp.nodes.defaults.numpy.mathematical.sin_node import SinNode
from cvp.nodes.defaults.numpy.mathematical.cos_node import CosNode
from cvp.nodes.defaults.numpy.mathematical.add_node import AddNode
from cvp.nodes.defaults.numpy.mathematical.subtract_node import SubtractNode
from cvp.nodes.defaults.numpy.mathematical.multiply_node import MultiplyNode
from cvp.nodes.defaults.numpy.mathematical.divide_node import DivideNode
from cvp.nodes.defaults.numpy.mathematical.sqrt_node import SqrtNode
from cvp.nodes.defaults.numpy.mathematical.exp_node import ExpNode
from cvp.nodes.defaults.numpy.mathematical.log_node import LogNode
from cvp.nodes.defaults.numpy.linalg.dot_node import DotNode
from cvp.nodes.defaults.numpy.linalg.matmul_node import MatmulNode
from cvp.nodes.defaults.numpy.logic.equal_node import EqualNode
from cvp.nodes.defaults.numpy.logic.greater_node import GreaterNode
from cvp.nodes.defaults.numpy.logic.logical_and_node import LogicalAndNode
from cvp.nodes.record import NodeRecord


class BasicNumpyNodesTestCase(TestCase):
    """Basic tests for numpy nodes to ensure they work correctly."""

    def setUp(self):
        self.record = NodeRecord.empty()
        warnings.filterwarnings("ignore")

    def test_numpy_nodes_count(self):
        """Test that we have the expected number of numpy nodes."""
        nodes = get_numpy_nodes()
        self.assertIsInstance(nodes, list)
        self.assertGreater(len(nodes), 150)
        print(f"Found {len(nodes)} numpy nodes")

    def test_mathematical_functions_basic(self):
        """Test basic mathematical functions."""
        # Test sin
        sin_node = SinNode()
        self.record.set(sin_node._input_pins[0], np.pi / 2)
        sin_node.run(self.record)
        result = self.record.get(sin_node._output)
        np.testing.assert_almost_equal(result, 1.0, decimal=5)

        # Test cos
        self.record = NodeRecord.empty()
        cos_node = CosNode()
        self.record.set(cos_node._input_pins[0], 0)
        cos_node.run(self.record)
        result = self.record.get(cos_node._output)
        np.testing.assert_almost_equal(result, 1.0, decimal=5)

        # Test sqrt
        self.record = NodeRecord.empty()
        sqrt_node = SqrtNode()
        self.record.set(sqrt_node._input_pins[0], 16)
        sqrt_node.run(self.record)
        result = self.record.get(sqrt_node._output)
        np.testing.assert_almost_equal(result, 4.0, decimal=5)

        # Test exp
        self.record = NodeRecord.empty()
        exp_node = ExpNode()
        self.record.set(exp_node._input_pins[0], 1)
        exp_node.run(self.record)
        result = self.record.get(exp_node._output)
        np.testing.assert_almost_equal(result, np.e, decimal=5)

        # Test log
        self.record = NodeRecord.empty()
        log_node = LogNode()
        self.record.set(log_node._input_pins[0], np.e)
        log_node.run(self.record)
        result = self.record.get(log_node._output)
        np.testing.assert_almost_equal(result, 1.0, decimal=5)

    def test_arithmetic_operations_basic(self):
        """Test basic arithmetic operations."""
        arr1 = np.array([1, 2, 3])
        arr2 = np.array([4, 5, 6])

        # Test add
        add_node = AddNode()
        self.record.set(add_node._input_pins[0], arr1)
        self.record.set(add_node._input_pins[1], arr2)
        add_node.run(self.record)
        result = self.record.get(add_node._output)
        expected = np.array([5, 7, 9])
        np.testing.assert_array_equal(result, expected)

        # Test subtract
        self.record = NodeRecord.empty()
        subtract_node = SubtractNode()
        self.record.set(subtract_node._input_pins[0], arr2)
        self.record.set(subtract_node._input_pins[1], arr1)
        subtract_node.run(self.record)
        result = self.record.get(subtract_node._output)
        expected = np.array([3, 3, 3])
        np.testing.assert_array_equal(result, expected)

        # Test multiply
        self.record = NodeRecord.empty()
        multiply_node = MultiplyNode()
        self.record.set(multiply_node._input_pins[0], arr1)
        self.record.set(multiply_node._input_pins[1], arr2)
        multiply_node.run(self.record)
        result = self.record.get(multiply_node._output)
        expected = np.array([4, 10, 18])
        np.testing.assert_array_equal(result, expected)

        # Test divide
        self.record = NodeRecord.empty()
        divide_node = DivideNode()
        self.record.set(divide_node._input_pins[0], arr2)
        self.record.set(divide_node._input_pins[1], arr1)
        divide_node.run(self.record)
        result = self.record.get(divide_node._output)
        expected = np.array([4, 2.5, 2])
        np.testing.assert_array_almost_equal(result, expected)

    def test_linear_algebra_basic(self):
        """Test basic linear algebra operations."""
        # Test dot product
        dot_node = DotNode()
        vec1 = np.array([1, 2, 3])
        vec2 = np.array([4, 5, 6])
        self.record.set(dot_node._input_pins[0], vec1)
        self.record.set(dot_node._input_pins[1], vec2)
        dot_node.run(self.record)
        result = self.record.get(dot_node._output)
        expected = np.dot(vec1, vec2)  # 1*4 + 2*5 + 3*6 = 32
        np.testing.assert_almost_equal(result, expected)

        # Test matrix multiplication
        self.record = NodeRecord.empty()
        matmul_node = MatmulNode()
        mat1 = np.array([[1, 2], [3, 4]])
        mat2 = np.array([[5, 6], [7, 8]])
        self.record.set(matmul_node._input_pins[0], mat1)
        self.record.set(matmul_node._input_pins[1], mat2)
        matmul_node.run(self.record)
        result = self.record.get(matmul_node._output)
        expected = np.matmul(mat1, mat2)
        np.testing.assert_array_equal(result, expected)

    def test_logic_operations_basic(self):
        """Test basic logic operations."""
        arr1 = np.array([1, 2, 3, 4])
        arr2 = np.array([1, 3, 2, 4])

        # Test equal
        equal_node = EqualNode()
        self.record.set(equal_node._input_pins[0], arr1)
        self.record.set(equal_node._input_pins[1], arr2)
        equal_node.run(self.record)
        result = self.record.get(equal_node._output)
        expected = np.equal(arr1, arr2)  # [True, False, False, True]
        np.testing.assert_array_equal(result, expected)

        # Test greater
        self.record = NodeRecord.empty()
        greater_node = GreaterNode()
        self.record.set(greater_node._input_pins[0], arr1)
        self.record.set(greater_node._input_pins[1], arr2)
        greater_node.run(self.record)
        result = self.record.get(greater_node._output)
        expected = np.greater(arr1, arr2)  # [False, False, True, False]
        np.testing.assert_array_equal(result, expected)

        # Test logical_and
        self.record = NodeRecord.empty()
        logical_and_node = LogicalAndNode()
        bool_arr1 = np.array([True, False, True, False])
        bool_arr2 = np.array([True, True, False, False])
        self.record.set(logical_and_node._input_pins[0], bool_arr1)
        self.record.set(logical_and_node._input_pins[1], bool_arr2)
        logical_and_node.run(self.record)
        result = self.record.get(logical_and_node._output)
        expected = np.logical_and(bool_arr1, bool_arr2)
        np.testing.assert_array_equal(result, expected)

    def test_complex_number_support(self):
        """Test that nodes support complex numbers."""
        # Test with complex input
        sin_node = SinNode()
        complex_input = 1 + 2j
        self.record.set(sin_node._input_pins[0], complex_input)
        sin_node.run(self.record)
        result = self.record.get(sin_node._output)
        expected = np.sin(complex_input)
        np.testing.assert_almost_equal(result, expected)

    def test_broadcasting_support(self):
        """Test that nodes support numpy broadcasting."""
        add_node = AddNode()
        # Broadcasting scalar with array
        scalar = 5
        array = np.array([1, 2, 3])
        self.record.set(add_node._input_pins[0], scalar)
        self.record.set(add_node._input_pins[1], array)
        add_node.run(self.record)
        result = self.record.get(add_node._output)
        expected = scalar + array  # [6, 7, 8]
        np.testing.assert_array_equal(result, expected)

    def test_error_cases(self):
        """Test error handling."""
        # Test sqrt with negative number
        sqrt_node = SqrtNode()
        try:
            self.record.set(sqrt_node._input_pins[0], -4)
            sqrt_node.run(self.record)
            result = self.record.get(sqrt_node._output)
            # Should produce NaN or complex result
            self.assertTrue(np.isnan(result) or np.iscomplexobj(result))
        except (ValueError, RuntimeWarning):
            # It's acceptable if this raises an error or warning
            pass

    def test_different_dtypes(self):
        """Test nodes with different data types."""
        add_node = AddNode()

        # Test with int arrays
        self.record = NodeRecord.empty()
        int_arr1 = np.array([1, 2, 3], dtype=np.int32)
        int_arr2 = np.array([4, 5, 6], dtype=np.int32)
        self.record.set(add_node._input_pins[0], int_arr1)
        self.record.set(add_node._input_pins[1], int_arr2)
        add_node.run(self.record)
        result = self.record.get(add_node._output)
        expected = int_arr1 + int_arr2
        np.testing.assert_array_equal(result, expected)

        # Test with float arrays
        self.record = NodeRecord.empty()
        float_arr1 = np.array([1.5, 2.5, 3.5], dtype=np.float32)
        float_arr2 = np.array([4.5, 5.5, 6.5], dtype=np.float32)
        self.record.set(add_node._input_pins[0], float_arr1)
        self.record.set(add_node._input_pins[1], float_arr2)
        add_node.run(self.record)
        result = self.record.get(add_node._output)
        expected = float_arr1 + float_arr2
        np.testing.assert_array_almost_equal(result, expected)

    def test_large_arrays(self):
        """Test with larger arrays to ensure performance is reasonable."""
        add_node = AddNode()
        # Create larger arrays
        large_arr1 = np.random.random(1000)
        large_arr2 = np.random.random(1000)

        self.record.set(add_node._input_pins[0], large_arr1)
        self.record.set(add_node._input_pins[1], large_arr2)
        add_node.run(self.record)
        result = self.record.get(add_node._output)
        expected = large_arr1 + large_arr2
        np.testing.assert_array_almost_equal(result, expected)

    def test_multidimensional_arrays(self):
        """Test with multidimensional arrays."""
        add_node = AddNode()
        # Test with 2D arrays
        arr2d_1 = np.array([[1, 2], [3, 4]])
        arr2d_2 = np.array([[5, 6], [7, 8]])

        self.record.set(add_node._input_pins[0], arr2d_1)
        self.record.set(add_node._input_pins[1], arr2d_2)
        add_node.run(self.record)
        result = self.record.get(add_node._output)
        expected = arr2d_1 + arr2d_2
        np.testing.assert_array_equal(result, expected)

    def test_node_structure(self):
        """Test that all tested nodes have proper structure."""
        from cvp.nodes.defaults.numpy._base import NumpyFunctionNode

        # Test a selection of nodes
        test_nodes = [SinNode(), AddNode(), DotNode(), EqualNode()]

        for node in test_nodes:
            # Check inheritance
            self.assertIsInstance(node, NumpyFunctionNode)

            # Check structure
            self.assertTrue(hasattr(node, '_input_pins'))
            self.assertTrue(hasattr(node, '_output'))
            self.assertGreater(len(node._input_pins), 0)

            # Check pin properties
            for pin in node._input_pins:
                self.assertTrue(hasattr(pin, 'name'))
                self.assertTrue(hasattr(pin, 'dtype'))

            output_pin = node._output
            self.assertTrue(hasattr(output_pin, 'name'))
            self.assertTrue(hasattr(output_pin, 'dtype'))


if __name__ == "__main__":
    main()