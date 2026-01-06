# -*- coding: utf-8 -*-

from unittest import TestCase, main

import numpy as np
import pandas as pd

from cvp.nodes.defaults.pandas.statistics.describe_node import DescribeNode
from cvp.nodes.record import NodeRecord


class DescribeNodeTestCase(TestCase):
    def setUp(self):
        self.node = DescribeNode()
        self.record = NodeRecord.empty()
        self.test_df = pd.DataFrame(
            {
                "numeric_int": [1, 2, 3, 4, 5],
                "numeric_float": [1.1, 2.2, 3.3, 4.4, 5.5],
                "string_col": ["a", "b", "c", "d", "e"],
                "boolean_col": [True, False, True, False, True],
            }
        )

    def test_describe_default(self):
        """Test describe with default settings."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)

        # By default, describe only includes numeric columns
        expected_cols = ["numeric_int", "numeric_float", "boolean_col"]
        for col in expected_cols:
            self.assertIn(col, result.columns)

        # Should not include string column by default
        self.assertNotIn("string_col", result.columns)

        # Should have standard statistical measures
        expected_stats = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
        for stat in expected_stats:
            self.assertIn(stat, result.index)

    def test_describe_numeric_columns(self):
        """Test describe statistics for numeric columns."""
        numeric_df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]})

        self.record.set(self.node._dataframe_pin, numeric_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)

        # Check specific statistics for column A
        self.assertEqual(result.loc["count", "A"], 5.0)
        self.assertEqual(result.loc["mean", "A"], 3.0)
        self.assertEqual(result.loc["min", "A"], 1.0)
        self.assertEqual(result.loc["max", "A"], 5.0)
        self.assertEqual(result.loc["50%", "A"], 3.0)  # Median

    def test_describe_include_all(self):
        """Test describe with include='all'."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._include_pin, "all")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)

        # Should include all columns
        for col in self.test_df.columns:
            self.assertIn(col, result.columns)

        # String column should have different statistics
        if "string_col" in result.columns:
            # For object/string columns, describe shows count, unique, top, freq
            self.assertIn("count", result.index)
            # Note: exact statistics depend on pandas version

    def test_describe_include_object(self):
        """Test describe with include='object'."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._include_pin, ["object"])
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)

        # Should only include object (string) columns
        self.assertIn("string_col", result.columns)
        self.assertNotIn("numeric_int", result.columns)
        self.assertNotIn("numeric_float", result.columns)

    def test_describe_exclude_int(self):
        """Test describe with exclude=['int64']."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._exclude_pin, ["int64"])
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)

        # Should exclude integer columns
        self.assertNotIn("numeric_int", result.columns)
        self.assertIn("numeric_float", result.columns)

    def test_describe_with_na_values(self):
        """Test describe with NaN values."""
        df_with_na = pd.DataFrame(
            {
                "A": [1, 2, None, 4, 5],
                "B": [10, None, None, 40, 50],
                "C": [1.0, 2.0, 3.0, 4.0, 5.0],
            }
        )

        self.record.set(self.node._dataframe_pin, df_with_na)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)

        # Count should reflect non-null values
        self.assertEqual(result.loc["count", "A"], 4.0)  # 4 non-null values
        self.assertEqual(result.loc["count", "B"], 3.0)  # 3 non-null values
        self.assertEqual(result.loc["count", "C"], 5.0)  # All non-null

    def test_describe_empty_dataframe(self):
        """Test describe on empty DataFrame."""
        empty_df = pd.DataFrame()

        self.record.set(self.node._dataframe_pin, empty_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)

    def test_describe_single_column(self):
        """Test describe on single column DataFrame."""
        single_col_df = pd.DataFrame({"values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})

        self.record.set(self.node._dataframe_pin, single_col_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result.columns), 1)
        self.assertIn("values", result.columns)

        # Check some expected statistics
        self.assertEqual(result.loc["count", "values"], 10.0)
        self.assertEqual(result.loc["mean", "values"], 5.5)
        self.assertEqual(result.loc["min", "values"], 1.0)
        self.assertEqual(result.loc["max", "values"], 10.0)

    def test_describe_constant_values(self):
        """Test describe with constant values."""
        constant_df = pd.DataFrame(
            {"constant": [5, 5, 5, 5, 5], "variable": [1, 2, 3, 4, 5]}
        )

        self.record.set(self.node._dataframe_pin, constant_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)

        # Constant column should have std=0
        self.assertEqual(result.loc["std", "constant"], 0.0)
        self.assertEqual(result.loc["min", "constant"], 5.0)
        self.assertEqual(result.loc["max", "constant"], 5.0)

    def test_describe_mixed_types(self):
        """Test describe with mixed data types."""
        mixed_df = pd.DataFrame(
            {
                "integers": [1, 2, 3],
                "floats": [1.1, 2.2, 3.3],
                "strings": ["x", "y", "z"],
                "booleans": [True, False, True],
                "dates": pd.date_range("2023-01-01", periods=3),
            }
        )

        self.record.set(self.node._dataframe_pin, mixed_df)
        self.record.set(self.node._include_pin, "all")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)

        # Should include all columns when include='all'
        for col in mixed_df.columns:
            self.assertIn(col, result.columns)

    def test_describe_large_dataset(self):
        """Test describe with larger dataset."""
        np.random.seed(42)
        large_df = pd.DataFrame(
            {
                "normal": np.random.normal(100, 15, 1000),
                "uniform": np.random.uniform(0, 100, 1000),
                "exponential": np.random.exponential(2, 1000),
            }
        )

        self.record.set(self.node._dataframe_pin, large_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result.columns), 3)

        # Count should be 1000 for all columns
        for col in large_df.columns:
            self.assertEqual(result.loc["count", col], 1000.0)

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_dataframe_pin"))
        self.assertTrue(hasattr(self.node, "_include_pin"))
        self.assertTrue(hasattr(self.node, "_exclude_pin"))
        self.assertTrue(hasattr(self.node, "_output"))

        self.assertEqual(self.node._include_pin.name.value, "include")
        self.assertEqual(self.node._exclude_pin.name.value, "exclude")

        self.assertTrue(self.node._dataframe_pin.required)
        self.assertFalse(self.node._include_pin.required)
        self.assertFalse(self.node._exclude_pin.required)


if __name__ == "__main__":
    main()
