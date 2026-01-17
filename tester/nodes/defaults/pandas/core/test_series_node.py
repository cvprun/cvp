# -*- coding: utf-8 -*-

from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas.core.series_node import SeriesNode
from cvp.nodes.record import NodeRecord


class SeriesNodeTestCase(TestCase):
    def setUp(self):
        self.node = SeriesNode()
        self.record = NodeRecord.empty()

    def test_series_from_list(self):
        """Test creating Series from list."""
        test_data = [1, 2, 3, 4, 5]

        self.record.set(self.node._data_pin, test_data)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), 5)
        self.assertEqual(result.tolist(), [1, 2, 3, 4, 5])

    def test_series_from_dict(self):
        """Test creating Series from dictionary."""
        test_data = {"a": 1, "b": 2, "c": 3}

        self.record.set(self.node._data_pin, test_data)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), 3)
        self.assertEqual(list(result.index), ["a", "b", "c"])
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"], 2)
        self.assertEqual(result["c"], 3)

    def test_series_with_custom_index(self):
        """Test creating Series with custom index."""
        test_data = [10, 20, 30]
        test_index = ["first", "second", "third"]

        self.record.set(self.node._data_pin, test_data)
        self.record.set(self.node._index_pin, test_index)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(list(result.index), ["first", "second", "third"])
        self.assertEqual(result["first"], 10)
        self.assertEqual(result["second"], 20)
        self.assertEqual(result["third"], 30)

    def test_series_with_name(self):
        """Test creating Series with name."""
        test_data = [1.1, 2.2, 3.3]
        test_name = "test_series"

        self.record.set(self.node._data_pin, test_data)
        self.record.set(self.node._name_pin, test_name)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result.name, "test_series")
        self.assertEqual(result.tolist(), [1.1, 2.2, 3.3])

    def test_series_with_index_and_name(self):
        """Test creating Series with both index and name."""
        test_data = ["a", "b", "c"]
        test_index = [1, 2, 3]
        test_name = "letters"

        self.record.set(self.node._data_pin, test_data)
        self.record.set(self.node._index_pin, test_index)
        self.record.set(self.node._name_pin, test_name)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result.name, "letters")
        self.assertEqual(list(result.index), [1, 2, 3])
        self.assertEqual(result[1], "a")
        self.assertEqual(result[3], "c")

    def test_series_from_scalar(self):
        """Test creating Series from scalar value."""
        test_data = 42

        self.record.set(self.node._data_pin, test_data)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0], 42)

    def test_series_from_numpy_array(self):
        """Test creating Series from numpy array."""
        import numpy as np

        test_data = np.array([1.5, 2.5, 3.5])

        self.record.set(self.node._data_pin, test_data)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result.iloc[0], 1.5)
        self.assertAlmostEqual(result.iloc[2], 3.5)

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_data_pin"))
        self.assertTrue(hasattr(self.node, "_index_pin"))
        self.assertTrue(hasattr(self.node, "_name_pin"))
        self.assertTrue(hasattr(self.node, "_output"))

        self.assertEqual(self.node._data_pin.name, "data")
        self.assertEqual(self.node._index_pin.name, "index")
        self.assertEqual(self.node._name_pin.name, "name")
        self.assertEqual(self.node._output.name, "series")

        # DataInputPin defaults to required=False unless explicitly set
        self.assertFalse(self.node._data_pin.required)
        self.assertFalse(self.node._index_pin.required)
        self.assertFalse(self.node._name_pin.required)


if __name__ == "__main__":
    main()
