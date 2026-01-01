# -*- coding: utf-8 -*-

from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas.core.dataframe_node import DataFrameNode
from cvp.nodes.record import NodeRecord


class DataFrameNodeTestCase(TestCase):
    def setUp(self):
        self.node = DataFrameNode()
        self.record = NodeRecord.empty()

    def test_dataframe_from_dict(self):
        """Test creating DataFrame from dictionary."""
        test_data = {"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]}

        self.record.set(self.node._data_pin, test_data)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B", "C"])
        self.assertEqual(len(result), 3)
        self.assertEqual(result["A"].tolist(), [1, 2, 3])
        self.assertEqual(result["B"].tolist(), [4, 5, 6])
        self.assertEqual(result["C"].tolist(), [7, 8, 9])

    def test_dataframe_from_list_of_lists(self):
        """Test creating DataFrame from list of lists."""
        test_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        self.record.set(self.node._data_pin, test_data)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)
        self.assertEqual(len(result.columns), 3)

    def test_dataframe_with_index(self):
        """Test creating DataFrame with custom index."""
        test_data = {"A": [1, 2, 3], "B": [4, 5, 6]}
        test_index = ["row1", "row2", "row3"]

        self.record.set(self.node._data_pin, test_data)
        self.record.set(self.node._index_pin, test_index)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.index), ["row1", "row2", "row3"])

    def test_dataframe_with_columns(self):
        """Test creating DataFrame with custom columns."""
        test_data = [[1, 2], [3, 4], [5, 6]]
        test_columns = ["col1", "col2"]

        self.record.set(self.node._data_pin, test_data)
        self.record.set(self.node._columns_pin, test_columns)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["col1", "col2"])

    def test_dataframe_with_index_and_columns(self):
        """Test creating DataFrame with both custom index and columns."""
        test_data = [[1, 2], [3, 4], [5, 6]]
        test_index = ["x", "y", "z"]
        test_columns = ["alpha", "beta"]

        self.record.set(self.node._data_pin, test_data)
        self.record.set(self.node._index_pin, test_index)
        self.record.set(self.node._columns_pin, test_columns)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.index), ["x", "y", "z"])
        self.assertEqual(list(result.columns), ["alpha", "beta"])
        self.assertEqual(result.loc["x", "alpha"], 1)
        self.assertEqual(result.loc["z", "beta"], 6)

    def test_dataframe_empty_dict(self):
        """Test creating DataFrame from empty dictionary."""
        test_data = {}

        self.record.set(self.node._data_pin, test_data)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_data_pin"))
        self.assertTrue(hasattr(self.node, "_index_pin"))
        self.assertTrue(hasattr(self.node, "_columns_pin"))
        self.assertTrue(hasattr(self.node, "_output"))

        self.assertEqual(self.node._data_pin.name.value, "data")
        self.assertEqual(self.node._index_pin.name.value, "index")
        self.assertEqual(self.node._columns_pin.name.value, "columns")
        self.assertEqual(self.node._output.name.value, "dataframe")

        self.assertTrue(self.node._data_pin.required)
        self.assertFalse(self.node._index_pin.required)
        self.assertFalse(self.node._columns_pin.required)


if __name__ == "__main__":
    main()