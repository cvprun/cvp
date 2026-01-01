# -*- coding: utf-8 -*-

from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas.manipulation.filter_node import FilterNode
from cvp.nodes.record import NodeRecord


class FilterNodeTestCase(TestCase):
    def setUp(self):
        self.node = FilterNode()
        self.record = NodeRecord.empty()
        self.test_df = pd.DataFrame({
            "A": [1, 2, 3, 4, 5],
            "B": [10, 20, 30, 40, 50],
            "C": ["a", "b", "c", "d", "e"],
            "D": [True, False, True, False, True]
        })

    def test_filter_simple_condition(self):
        """Test filtering with simple numeric condition."""
        condition = self.test_df["A"] > 3

        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._condition_pin, condition)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)  # Values 4, 5
        self.assertEqual(result["A"].tolist(), [4, 5])
        self.assertEqual(result["B"].tolist(), [40, 50])

    def test_filter_equality_condition(self):
        """Test filtering with equality condition."""
        condition = self.test_df["C"] == "c"

        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._condition_pin, condition)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 1)
        self.assertEqual(result["A"].iloc[0], 3)
        self.assertEqual(result["C"].iloc[0], "c")

    def test_filter_boolean_column(self):
        """Test filtering with boolean column."""
        condition = self.test_df["D"]

        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._condition_pin, condition)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)  # True values at indices 0, 2, 4
        self.assertEqual(result["A"].tolist(), [1, 3, 5])

    def test_filter_multiple_conditions(self):
        """Test filtering with multiple conditions."""
        condition = (self.test_df["A"] > 2) & (self.test_df["B"] < 45)

        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._condition_pin, condition)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)  # Values where A > 2 and B < 45 (A=3,4)
        self.assertEqual(result["A"].tolist(), [3, 4])

    def test_filter_isin_condition(self):
        """Test filtering with isin condition."""
        condition = self.test_df["C"].isin(["a", "c", "e"])

        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._condition_pin, condition)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)
        self.assertEqual(result["C"].tolist(), ["a", "c", "e"])

    def test_filter_string_contains(self):
        """Test filtering with string contains."""
        # Add more complex string data
        df_strings = pd.DataFrame({
            "names": ["Alice Smith", "Bob Johnson", "Charlie Brown", "David Smith"],
            "values": [10, 20, 30, 40]
        })
        condition = df_strings["names"].str.contains("Smith")

        self.record.set(self.node._dataframe_pin, df_strings)
        self.record.set(self.node._condition_pin, condition)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertEqual(result["names"].tolist(), ["Alice Smith", "David Smith"])

    def test_filter_no_matches(self):
        """Test filtering with condition that matches no rows."""
        condition = self.test_df["A"] > 10

        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._condition_pin, condition)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 0)
        self.assertEqual(list(result.columns), ["A", "B", "C", "D"])

    def test_filter_all_matches(self):
        """Test filtering with condition that matches all rows."""
        condition = self.test_df["A"] > 0

        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._condition_pin, condition)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 5)
        pd.testing.assert_frame_equal(result, self.test_df)

    def test_filter_with_na_values(self):
        """Test filtering with NaN values."""
        df_with_na = pd.DataFrame({
            "A": [1, 2, None, 4, 5],
            "B": [10, None, 30, 40, 50]
        })
        condition = df_with_na["A"] > 2

        self.record.set(self.node._dataframe_pin, df_with_na)
        self.record.set(self.node._condition_pin, condition)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        # Should only include rows where A > 2 and A is not NaN
        self.assertEqual(len(result), 2)  # A=4, A=5
        self.assertEqual(result["A"].tolist(), [4.0, 5.0])

    def test_filter_empty_dataframe(self):
        """Test filtering empty DataFrame."""
        empty_df = pd.DataFrame(columns=["A", "B"])
        condition = pd.Series([], dtype=bool)

        self.record.set(self.node._dataframe_pin, empty_df)
        self.record.set(self.node._condition_pin, condition)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_dataframe_pin"))
        self.assertTrue(hasattr(self.node, "_condition_pin"))
        self.assertTrue(hasattr(self.node, "_output"))

        self.assertEqual(self.node._dataframe_pin.name.value, "dataframe")
        self.assertEqual(self.node._condition_pin.name.value, "condition")
        self.assertEqual(self.node._output.name.value, "result")

        self.assertTrue(self.node._dataframe_pin.required)
        self.assertTrue(self.node._condition_pin.required)


if __name__ == "__main__":
    main()