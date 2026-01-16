# -*- coding: utf-8 -*-

from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas.manipulation.select_node import SelectNode
from cvp.nodes.record import NodeRecord


class SelectNodeTestCase(TestCase):
    def setUp(self):
        self.node = SelectNode()
        self.record = NodeRecord.empty()
        self.test_df = pd.DataFrame(
            {
                "A": [1, 2, 3, 4],
                "B": [5, 6, 7, 8],
                "C": [9, 10, 11, 12],
                "D": ["a", "b", "c", "d"],
            }
        )

    def test_select_single_column(self):
        """Test selecting a single column."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._columns_pin, "A")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result.name, "A")
        self.assertEqual(result.tolist(), [1, 2, 3, 4])

    def test_select_multiple_columns(self):
        """Test selecting multiple columns."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._columns_pin, ["A", "C"])
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "C"])
        self.assertEqual(len(result), 4)
        self.assertEqual(result["A"].tolist(), [1, 2, 3, 4])
        self.assertEqual(result["C"].tolist(), [9, 10, 11, 12])

    def test_select_all_columns(self):
        """Test selecting all columns."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._columns_pin, ["A", "B", "C", "D"])
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B", "C", "D"])
        pd.testing.assert_frame_equal(result, self.test_df)

    def test_select_string_column(self):
        """Test selecting string column."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._columns_pin, "D")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result.name, "D")
        self.assertEqual(result.tolist(), ["a", "b", "c", "d"])

    def test_select_reordered_columns(self):
        """Test selecting columns in different order."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._columns_pin, ["D", "A", "B"])
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["D", "A", "B"])
        self.assertEqual(result["D"].tolist(), ["a", "b", "c", "d"])
        self.assertEqual(result["A"].tolist(), [1, 2, 3, 4])
        self.assertEqual(result["B"].tolist(), [5, 6, 7, 8])

    def test_select_empty_dataframe(self):
        """Test selecting from empty DataFrame."""
        empty_df = pd.DataFrame()
        self.record.set(self.node._dataframe_pin, empty_df)
        self.record.set(self.node._columns_pin, [])
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_dataframe_pin"))
        self.assertTrue(hasattr(self.node, "_columns_pin"))
        self.assertTrue(hasattr(self.node, "_output"))

        self.assertEqual(self.node._dataframe_pin.name.value, "dataframe")
        self.assertEqual(self.node._columns_pin.name.value, "columns")
        self.assertEqual(self.node._output.name.value, "result")

        self.assertTrue(self.node._dataframe_pin.required)
        self.assertTrue(self.node._columns_pin.required)


if __name__ == "__main__":
    main()
