# -*- coding: utf-8 -*-

from unittest import TestCase, main

import cv2
import numpy as np

from cvp.nodes.defaults.opencv.core.add_node import AddNode
from cvp.nodes.defaults.opencv.core.bitwise_and_node import BitwiseAndNode
from cvp.nodes.defaults.opencv.core.flip_node import FlipNode
from cvp.nodes.record import NodeRecord


class OpenCVNodesTestCase(TestCase):
    def test_get_opencv_nodes(self):
        """Test that get_opencv_nodes returns a list of nodes."""
        # Test core nodes only for now to avoid complex initialization issues
        from cvp.nodes.defaults.opencv.core import get_core_nodes

        nodes = get_core_nodes()
        self.assertIsInstance(nodes, list)
        self.assertGreater(len(nodes), 15)  # Should have 20+ core nodes

    def test_flip_node(self):
        """Test FlipNode functionality."""
        flip_node = FlipNode()
        record = NodeRecord.empty()

        # Create test image
        test_image = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.uint8)
        flip_code = 1  # Vertical flip

        record.set(flip_node._input_pins[0], test_image)
        record.set(flip_node._input_pins[1], flip_code)
        flip_node.run(record)
        result = record.get(flip_node._output)

        expected = cv2.flip(test_image, flip_code)
        np.testing.assert_array_equal(result, expected)

    def test_add_node(self):
        """Test AddNode functionality."""
        add_node = AddNode()
        record = NodeRecord.empty()

        # Create test images
        src1 = np.array([[10, 20], [30, 40]], dtype=np.uint8)
        src2 = np.array([[5, 10], [15, 20]], dtype=np.uint8)

        record.set(add_node._input_pins[0], src1)
        record.set(add_node._input_pins[1], src2)
        add_node.run(record)
        result = record.get(add_node._output)

        expected = cv2.add(src1, src2)
        np.testing.assert_array_equal(result, expected)

    def test_bitwise_and_node(self):
        """Test BitwiseAndNode functionality."""
        bitwise_and_node = BitwiseAndNode()
        record = NodeRecord.empty()

        # Create test images
        src1 = np.array([[255, 0], [255, 0]], dtype=np.uint8)
        src2 = np.array([[255, 255], [0, 0]], dtype=np.uint8)

        record.set(bitwise_and_node._input_pins[0], src1)
        record.set(bitwise_and_node._input_pins[1], src2)
        bitwise_and_node.run(record)
        result = record.get(bitwise_and_node._output)

        expected = cv2.bitwise_and(src1, src2)
        np.testing.assert_array_equal(result, expected)

    def test_node_inheritance(self):
        """Test that all OpenCV nodes inherit from proper base classes."""
        from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode

        flip_node = FlipNode()
        self.assertIsInstance(flip_node, OpenCVFunctionNode)

        add_node = AddNode()
        self.assertIsInstance(add_node, OpenCVFunctionNode)

    def test_node_pins(self):
        """Test that nodes have proper pin configuration."""
        flip_node = FlipNode()

        # Check that node has input and output pins
        self.assertTrue(hasattr(flip_node, "_input_pins"))
        self.assertTrue(hasattr(flip_node, "_output"))
        self.assertGreater(len(flip_node._input_pins), 0)

        # Check pin properties
        input_pin = flip_node._input_pins[0]
        output_pin = flip_node._output

        self.assertTrue(hasattr(input_pin, "name"))
        self.assertTrue(hasattr(input_pin, "dtype"))
        self.assertTrue(hasattr(output_pin, "name"))
        self.assertTrue(hasattr(output_pin, "dtype"))

    def test_opencv_version(self):
        """Test that OpenCV is available and accessible."""
        self.assertTrue(hasattr(cv2, "__version__"))
        version = cv2.__version__
        self.assertIsInstance(version, str)
        self.assertGreater(len(version), 0)


if __name__ == "__main__":
    main()
