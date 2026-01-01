# -*- coding: utf-8 -*-

from unittest import TestCase

import numpy as np

from cvp.nodes.defaults.numpy.array_manipulation.concatenate_node import ConcatenateNode
from cvp.nodes.defaults.numpy.array_manipulation.dsplit_node import DsplitNode
from cvp.nodes.defaults.numpy.array_manipulation.dstack_node import DstackNode
from cvp.nodes.defaults.numpy.array_manipulation.expand_dims_node import ExpandDimsNode
from cvp.nodes.defaults.numpy.array_manipulation.flatten_node import FlattenNode
from cvp.nodes.defaults.numpy.array_manipulation.flip_node import FlipNode
from cvp.nodes.defaults.numpy.array_manipulation.fliplr_node import FliplrNode
from cvp.nodes.defaults.numpy.array_manipulation.flipud_node import FlipudNode
from cvp.nodes.defaults.numpy.array_manipulation.hsplit_node import HsplitNode
from cvp.nodes.defaults.numpy.array_manipulation.hstack_node import HstackNode
from cvp.nodes.defaults.numpy.array_manipulation.moveaxis_node import MoveaxisNode
from cvp.nodes.defaults.numpy.array_manipulation.ravel_node import RavelNode
from cvp.nodes.defaults.numpy.array_manipulation.repeat_node import RepeatNode
from cvp.nodes.defaults.numpy.array_manipulation.reshape_node import ReshapeNode
from cvp.nodes.defaults.numpy.array_manipulation.split_node import SplitNode
from cvp.nodes.defaults.numpy.array_manipulation.squeeze_node import SqueezeNode
from cvp.nodes.defaults.numpy.array_manipulation.stack_node import StackNode
from cvp.nodes.defaults.numpy.array_manipulation.swapaxes_node import SwapaxesNode
from cvp.nodes.defaults.numpy.array_manipulation.tile_node import TileNode
from cvp.nodes.defaults.numpy.array_manipulation.transpose_node import TransposeNode
from cvp.nodes.defaults.numpy.array_manipulation.vsplit_node import VsplitNode
from cvp.nodes.defaults.numpy.array_manipulation.vstack_node import VstackNode
from cvp.nodes.record import NodeRecord


class TestArrayManipulationNodes(TestCase):

    def setUp(self):
        self.record = NodeRecord.empty()
        self.test_array = np.array([[1, 2, 3], [4, 5, 6]])

    def test_concatenate_node(self):
        """Test ConcatenateNode functionality."""
        node = ConcatenateNode()

        # Test concatenation along axis 0
        arr1 = np.array([[1, 2], [3, 4]])
        arr2 = np.array([[5, 6]])
        arrays = [arr1, arr2]

        self.record.set(node._input_pins[0], arrays)
        self.record.set(node._input_pins[1], 0)  # axis
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.concatenate([arr1, arr2], axis=0)
        np.testing.assert_array_equal(result, expected)

    def test_expand_dims_node(self):
        """Test ExpandDimsNode functionality."""
        node = ExpandDimsNode()

        # Test expanding dimensions
        arr = np.array([1, 2, 3])
        self.record.set(node._input_pins[0], arr)
        self.record.set(node._input_pins[1], 0)  # axis
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.expand_dims(arr, axis=0)
        np.testing.assert_array_equal(result, expected)
        self.assertEqual(result.shape, (1, 3))

    def test_flatten_node(self):
        """Test FlattenNode functionality."""
        node = FlattenNode()

        # Test flattening array
        self.record.set(node._input_pins[0], self.test_array)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = self.test_array.flatten()
        np.testing.assert_array_equal(result, expected)

    def test_flip_node(self):
        """Test FlipNode functionality."""
        node = FlipNode()

        # Test flipping array
        self.record.set(node._input_pins[0], self.test_array)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.flip(self.test_array)
        np.testing.assert_array_equal(result, expected)

    def test_fliplr_node(self):
        """Test FliplrNode functionality."""
        node = FliplrNode()

        # Test left-right flip
        self.record.set(node._input_pins[0], self.test_array)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.fliplr(self.test_array)
        np.testing.assert_array_equal(result, expected)

    def test_flipud_node(self):
        """Test FlipudNode functionality."""
        node = FlipudNode()

        # Test up-down flip
        self.record.set(node._input_pins[0], self.test_array)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.flipud(self.test_array)
        np.testing.assert_array_equal(result, expected)

    def test_hstack_node(self):
        """Test HstackNode functionality."""
        node = HstackNode()

        # Test horizontal stacking
        arr1 = np.array([1, 2, 3])
        arr2 = np.array([4, 5, 6])
        arrays = [arr1, arr2]

        self.record.set(node._input_pins[0], arrays)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.hstack(arrays)
        np.testing.assert_array_equal(result, expected)

    def test_vstack_node(self):
        """Test VstackNode functionality."""
        node = VstackNode()

        # Test vertical stacking
        arr1 = np.array([1, 2, 3])
        arr2 = np.array([4, 5, 6])
        arrays = [arr1, arr2]

        self.record.set(node._input_pins[0], arrays)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.vstack(arrays)
        np.testing.assert_array_equal(result, expected)

    def test_dstack_node(self):
        """Test DstackNode functionality."""
        node = DstackNode()

        # Test depth stacking
        arr1 = np.array([[1, 2], [3, 4]])
        arr2 = np.array([[5, 6], [7, 8]])
        arrays = [arr1, arr2]

        self.record.set(node._input_pins[0], arrays)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.dstack(arrays)
        np.testing.assert_array_equal(result, expected)

    def test_reshape_node(self):
        """Test ReshapeNode functionality."""
        node = ReshapeNode()

        # Test reshaping
        arr = np.array([1, 2, 3, 4, 5, 6])
        new_shape = (2, 3)
        self.record.set(node._input_pins[0], arr)
        self.record.set(node._input_pins[1], new_shape)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = arr.reshape(new_shape)
        np.testing.assert_array_equal(result, expected)

    def test_ravel_node(self):
        """Test RavelNode functionality."""
        node = RavelNode()

        # Test raveling array
        self.record.set(node._input_pins[0], self.test_array)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.ravel(self.test_array)
        np.testing.assert_array_equal(result, expected)

    def test_squeeze_node(self):
        """Test SqueezeNode functionality."""
        node = SqueezeNode()

        # Test squeezing array
        arr = np.array([[[1], [2], [3]]])
        self.record.set(node._input_pins[0], arr)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.squeeze(arr)
        np.testing.assert_array_equal(result, expected)

    def test_stack_node(self):
        """Test StackNode functionality."""
        node = StackNode()

        # Test stacking arrays
        arr1 = np.array([1, 2, 3])
        arr2 = np.array([4, 5, 6])
        arrays = [arr1, arr2]

        self.record.set(node._input_pins[0], arrays)
        self.record.set(node._input_pins[1], 0)  # axis
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.stack(arrays, axis=0)
        np.testing.assert_array_equal(result, expected)

    def test_swapaxes_node(self):
        """Test SwapaxesNode functionality."""
        node = SwapaxesNode()

        # Test swapping axes
        arr = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        self.record.set(node._input_pins[0], arr)
        self.record.set(node._input_pins[1], 0)  # axis1
        self.record.set(node._input_pins[2], 1)  # axis2
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.swapaxes(arr, 0, 1)
        np.testing.assert_array_equal(result, expected)

    def test_tile_node(self):
        """Test TileNode functionality."""
        node = TileNode()

        # Test tiling array
        arr = np.array([1, 2])
        reps = 3
        self.record.set(node._input_pins[0], arr)
        self.record.set(node._input_pins[1], reps)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.tile(arr, reps)
        np.testing.assert_array_equal(result, expected)

    def test_transpose_node(self):
        """Test TransposeNode functionality."""
        node = TransposeNode()

        # Test transposing array
        self.record.set(node._input_pins[0], self.test_array)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.transpose(self.test_array)
        np.testing.assert_array_equal(result, expected)

    def test_repeat_node(self):
        """Test RepeatNode functionality."""
        node = RepeatNode()

        # Test repeating array elements
        arr = np.array([1, 2, 3])
        repeats = 2
        self.record.set(node._input_pins[0], arr)
        self.record.set(node._input_pins[1], repeats)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.repeat(arr, repeats)
        np.testing.assert_array_equal(result, expected)

    def test_moveaxis_node(self):
        """Test MoveaxisNode functionality."""
        node = MoveaxisNode()

        # Test moving axes
        arr = np.ones((3, 4, 5))
        self.record.set(node._input_pins[0], arr)
        self.record.set(node._input_pins[1], 0)  # source
        self.record.set(node._input_pins[2], -1)  # destination
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.moveaxis(arr, 0, -1)
        self.assertEqual(result.shape, expected.shape)

    def test_split_node(self):
        """Test SplitNode functionality."""
        node = SplitNode()

        # Test splitting array
        arr = np.array([1, 2, 3, 4, 5, 6])
        indices_or_sections = 2
        self.record.set(node._input_pins[0], arr)
        self.record.set(node._input_pins[1], indices_or_sections)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.split(arr, indices_or_sections)
        self.assertEqual(len(result), len(expected))
        for r, e in zip(result, expected):
            np.testing.assert_array_equal(r, e)

    def test_hsplit_node(self):
        """Test HsplitNode functionality."""
        node = HsplitNode()

        # Test horizontal splitting
        arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
        indices_or_sections = 2
        self.record.set(node._input_pins[0], arr)
        self.record.set(node._input_pins[1], indices_or_sections)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.hsplit(arr, indices_or_sections)
        self.assertEqual(len(result), len(expected))
        for r, e in zip(result, expected):
            np.testing.assert_array_equal(r, e)

    def test_vsplit_node(self):
        """Test VsplitNode functionality."""
        node = VsplitNode()

        # Test vertical splitting
        arr = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        indices_or_sections = 2
        self.record.set(node._input_pins[0], arr)
        self.record.set(node._input_pins[1], indices_or_sections)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.vsplit(arr, indices_or_sections)
        self.assertEqual(len(result), len(expected))
        for r, e in zip(result, expected):
            np.testing.assert_array_equal(r, e)

    def test_dsplit_node(self):
        """Test DsplitNode functionality."""
        node = DsplitNode()

        # Test depth splitting
        arr = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        indices_or_sections = 2
        self.record.set(node._input_pins[0], arr)
        self.record.set(node._input_pins[1], indices_or_sections)
        node.run(self.record)
        result = self.record.get(node._output)
        expected = np.dsplit(arr, indices_or_sections)
        self.assertEqual(len(result), len(expected))
        for r, e in zip(result, expected):
            np.testing.assert_array_equal(r, e)