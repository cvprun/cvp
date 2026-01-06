# -*- coding: utf-8 -*-

from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas.groupby.groupby_node import GroupByNode
from cvp.nodes.record import NodeRecord


class GroupByNodeTestCase(TestCase):
    def setUp(self):
        self.node = GroupByNode()
        self.record = NodeRecord.empty()
        self.test_df = pd.DataFrame(
            {
                "category": ["A", "B", "A", "B", "A", "C"],
                "value1": [10, 20, 15, 25, 12, 30],
                "value2": [1, 2, 3, 4, 5, 6],
                "group_col": ["X", "Y", "X", "Y", "X", "Z"],
            }
        )

    def test_groupby_single_column(self):
        """Test groupby with single column."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._by_pin, "category")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.core.groupby.DataFrameGroupBy)

        # Test that we can use the groupby object
        groups = list(result)
        group_names = [name for name, group in groups]
        self.assertIn("A", group_names)
        self.assertIn("B", group_names)
        self.assertIn("C", group_names)

    def test_groupby_multiple_columns(self):
        """Test groupby with multiple columns."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._by_pin, ["category", "group_col"])
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.core.groupby.DataFrameGroupBy)

        # Test groupby operations
        groups = list(result)
        self.assertGreater(len(groups), 0)

        # Should have combinations like ("A", "X"), ("B", "Y"), etc.
        group_keys = [name for name, group in groups]
        self.assertIn(("A", "X"), group_keys)

    def test_groupby_with_axis(self):
        """Test groupby with specified axis."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._by_pin, "category")
        self.record.set(self.node._axis_pin, 0)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.core.groupby.DataFrameGroupBy)

    def test_groupby_sort_false(self):
        """Test groupby with sort=False."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._by_pin, "category")
        self.record.set(self.node._sort_pin, False)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.core.groupby.DataFrameGroupBy)

    def test_groupby_with_lambda(self):
        """Test groupby with lambda function."""

        # Create simple test for lambda - group by whether value1 is > 15
        def group_func(x):
            return "high" if x > 15 else "low"

        # Map the function to the DataFrame index to create groupby series
        group_series = self.test_df["value1"].apply(group_func)

        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._by_pin, group_series)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.core.groupby.DataFrameGroupBy)

        groups = list(result)
        group_names = [name for name, group in groups]
        self.assertIn("high", group_names)
        self.assertIn("low", group_names)

    def test_groupby_numeric_aggregation(self):
        """Test groupby with common aggregation operations."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._by_pin, "category")
        self.node.run(self.record)
        groupby_obj = self.record.get(self.node._output)

        # Test common operations on the groupby object
        mean_result = groupby_obj.mean()
        self.assertIsInstance(mean_result, pd.DataFrame)

        sum_result = groupby_obj.sum()
        self.assertIsInstance(sum_result, pd.DataFrame)

        count_result = groupby_obj.count()
        self.assertIsInstance(count_result, pd.DataFrame)

        # Check that category A appears in results
        self.assertIn("A", mean_result.index)
        self.assertIn("A", sum_result.index)

    def test_groupby_size_operation(self):
        """Test groupby size operation."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._by_pin, "category")
        self.node.run(self.record)
        groupby_obj = self.record.get(self.node._output)

        size_result = groupby_obj.size()
        self.assertIsInstance(size_result, pd.Series)

        # Category A should have 3 entries, B should have 2, C should have 1
        self.assertEqual(size_result["A"], 3)
        self.assertEqual(size_result["B"], 2)
        self.assertEqual(size_result["C"], 1)

    def test_groupby_specific_column_aggregation(self):
        """Test groupby aggregation on specific columns."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._by_pin, "category")
        self.node.run(self.record)
        groupby_obj = self.record.get(self.node._output)

        # Aggregate only value1 column
        value1_mean = groupby_obj["value1"].mean()
        self.assertIsInstance(value1_mean, pd.Series)

        # Category A: (10+15+12)/3 = 12.33
        self.assertAlmostEqual(value1_mean["A"], 12.333333333333334, places=5)
        # Category B: (20+25)/2 = 22.5
        self.assertAlmostEqual(value1_mean["B"], 22.5, places=5)

    def test_groupby_empty_dataframe(self):
        """Test groupby with empty DataFrame."""
        empty_df = pd.DataFrame(columns=["category", "value"])

        self.record.set(self.node._dataframe_pin, empty_df)
        self.record.set(self.node._by_pin, "category")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.core.groupby.DataFrameGroupBy)

        # Empty groupby should have no groups
        groups = list(result)
        self.assertEqual(len(groups), 0)

    def test_groupby_single_group(self):
        """Test groupby where all rows belong to same group."""
        single_group_df = pd.DataFrame(
            {"category": ["A", "A", "A"], "value": [1, 2, 3]}
        )

        self.record.set(self.node._dataframe_pin, single_group_df)
        self.record.set(self.node._by_pin, "category")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.core.groupby.DataFrameGroupBy)

        groups = list(result)
        self.assertEqual(len(groups), 1)
        name, group = groups[0]
        self.assertEqual(name, "A")
        self.assertEqual(len(group), 3)

    def test_groupby_with_na_values(self):
        """Test groupby with NaN values in grouping column."""
        df_with_na = pd.DataFrame(
            {"category": ["A", None, "A", "B", None], "value": [1, 2, 3, 4, 5]}
        )

        self.record.set(self.node._dataframe_pin, df_with_na)
        self.record.set(self.node._by_pin, "category")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.core.groupby.DataFrameGroupBy)

        # By default, NaN values are excluded from grouping
        groups = list(result)
        group_names = [name for name, group in groups]
        self.assertIn("A", group_names)
        self.assertIn("B", group_names)
        # NaN group may or may not be included depending on pandas version

    def test_groupby_index_grouping(self):
        """Test groupby using DataFrame index."""
        indexed_df = self.test_df.set_index("category")

        self.record.set(self.node._dataframe_pin, indexed_df)
        self.record.set(self.node._by_pin, level=0)  # Group by index level
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.core.groupby.DataFrameGroupBy)

    def test_groupby_datetime_grouping(self):
        """Test groupby with datetime data."""
        datetime_df = pd.DataFrame(
            {
                "date": pd.date_range("2023-01-01", periods=6, freq="D"),
                "value": [1, 2, 3, 4, 5, 6],
            }
        )
        # Group by day of week
        datetime_df["day_of_week"] = datetime_df["date"].dt.day_name()

        self.record.set(self.node._dataframe_pin, datetime_df)
        self.record.set(self.node._by_pin, "day_of_week")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.core.groupby.DataFrameGroupBy)

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_dataframe_pin"))
        self.assertTrue(hasattr(self.node, "_by_pin"))
        self.assertTrue(hasattr(self.node, "_axis_pin"))
        self.assertTrue(hasattr(self.node, "_sort_pin"))
        self.assertTrue(hasattr(self.node, "_output"))

        self.assertEqual(self.node._by_pin.name.value, "by")
        self.assertEqual(self.node._axis_pin.name.value, "axis")
        self.assertEqual(self.node._sort_pin.name.value, "sort")

        self.assertTrue(self.node._dataframe_pin.required)
        self.assertTrue(self.node._by_pin.required)
        self.assertFalse(self.node._axis_pin.required)
        self.assertFalse(self.node._sort_pin.required)


if __name__ == "__main__":
    main()
