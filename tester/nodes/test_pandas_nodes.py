# -*- coding: utf-8 -*-

from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas import get_pandas_nodes
from cvp.nodes.defaults.pandas.core.dataframe_node import DataFrameNode
from cvp.nodes.defaults.pandas.core.series_node import SeriesNode
from cvp.nodes.defaults.pandas.manipulation.select_node import SelectNode
from cvp.nodes.defaults.pandas.statistics.mean_node import MeanNode
from cvp.nodes.record import NodeRecord


class PandasNodesTestCase(TestCase):
    def test_get_pandas_nodes(self):
        """Test that get_pandas_nodes returns a list of nodes."""
        nodes = get_pandas_nodes()
        self.assertIsInstance(nodes, list)
        self.assertGreater(len(nodes), 10)  # Should have multiple nodes

    def test_dataframe_node(self):
        """Test DataFrameNode functionality."""
        df_node = DataFrameNode()
        record = NodeRecord.empty()

        # Test with dict input
        test_data = {"A": [1, 2, 3], "B": [4, 5, 6]}
        record.set(df_node._data_pin, test_data)
        df_node.run(record)
        result = record.get(df_node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B"])
        self.assertEqual(len(result), 3)

    def test_series_node(self):
        """Test SeriesNode functionality."""
        series_node = SeriesNode()
        record = NodeRecord.empty()

        # Test with list input
        test_data = [1, 2, 3, 4, 5]
        record.set(series_node._data_pin, test_data)
        series_node.run(record)
        result = record.get(series_node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), 5)
        self.assertEqual(result.tolist(), [1, 2, 3, 4, 5])

    def test_select_node(self):
        """Test SelectNode functionality."""
        select_node = SelectNode()
        record = NodeRecord.empty()

        # Create test DataFrame
        test_df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
        record.set(select_node._dataframe_pin, test_df)
        record.set(select_node._columns_pin, "A")
        select_node.run(record)
        result = record.get(select_node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result.name, "A")
        self.assertEqual(result.tolist(), [1, 2, 3])

        # Test multiple column selection
        record_multi = NodeRecord.empty()
        record_multi.set(select_node._dataframe_pin, test_df)
        record_multi.set(select_node._columns_pin, ["A", "C"])
        select_node.run(record_multi)
        result_multi = record_multi.get(select_node._output)

        self.assertIsInstance(result_multi, pd.DataFrame)
        self.assertEqual(list(result_multi.columns), ["A", "C"])

    def test_mean_node(self):
        """Test MeanNode functionality."""
        mean_node = MeanNode()
        record = NodeRecord.empty()

        # Create test DataFrame
        test_df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        record.set(mean_node._dataframe_pin, test_df)
        mean_node.run(record)
        result = record.get(mean_node._output)

        expected = pd.Series([2.0, 5.0], index=["A", "B"])
        pd.testing.assert_series_equal(result, expected)

    def test_node_inheritance(self):
        """Test that pandas nodes inherit from proper base classes."""
        from cvp.nodes.defaults.pandas._base import DataFrameMethodNode

        mean_node = MeanNode()
        self.assertIsInstance(mean_node, DataFrameMethodNode)

    def test_node_pins(self):
        """Test that nodes have proper pin configuration."""
        df_node = DataFrameNode()

        # Check that node has input and output pins
        self.assertTrue(hasattr(df_node, "_data_pin"))
        self.assertTrue(hasattr(df_node, "_output"))

        # Check pin properties
        data_pin = df_node._data_pin
        output_pin = df_node._output

        self.assertTrue(hasattr(data_pin, "name"))
        self.assertTrue(hasattr(data_pin, "dtype"))
        self.assertTrue(hasattr(output_pin, "name"))
        self.assertTrue(hasattr(output_pin, "dtype"))

    def test_dataframe_with_optional_params(self):
        """Test DataFrameNode with optional parameters."""
        df_node = DataFrameNode()
        record = NodeRecord.empty()

        # Test with data, index, and columns
        test_data = [[1, 2], [3, 4], [5, 6]]
        test_index = ["row1", "row2", "row3"]
        test_columns = ["col1", "col2"]

        record.set(df_node._data_pin, test_data)
        record.set(df_node._index_pin, test_index)
        record.set(df_node._columns_pin, test_columns)
        df_node.run(record)
        result = record.get(df_node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["col1", "col2"])
        self.assertEqual(list(result.index), ["row1", "row2", "row3"])

    def test_series_with_optional_params(self):
        """Test SeriesNode with optional parameters."""
        series_node = SeriesNode()
        record = NodeRecord.empty()

        # Test with data, index, and name
        test_data = [10, 20, 30]
        test_index = ["a", "b", "c"]
        test_name = "test_series"

        record.set(series_node._data_pin, test_data)
        record.set(series_node._index_pin, test_index)
        record.set(series_node._name_pin, test_name)
        series_node.run(record)
        result = record.get(series_node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result.name, "test_series")
        self.assertEqual(list(result.index), ["a", "b", "c"])
        self.assertEqual(result.tolist(), [10, 20, 30])


if __name__ == "__main__":
    main()
