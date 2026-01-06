# -*- coding: utf-8 -*-

from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas.statistics.corr_node import CorrNode
from cvp.nodes.record import NodeRecord


class CorrNodeTestCase(TestCase):
    def setUp(self):
        self.node = CorrNode()
        self.record = NodeRecord.empty()
        self.test_df = pd.DataFrame(
            {
                "A": [1, 2, 3, 4, 5],
                "B": [2, 4, 6, 8, 10],  # Perfect positive correlation with A
                "C": [5, 4, 3, 2, 1],  # Perfect negative correlation with A
                "D": [1, 3, 2, 5, 4],  # Some correlation
            }
        )

    def test_corr_default_pearson(self):
        """Test correlation calculation with default Pearson method."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (4, 4))  # 4x4 correlation matrix

        # Perfect positive correlation between A and B
        self.assertAlmostEqual(result.loc["A", "B"], 1.0, places=5)
        self.assertAlmostEqual(result.loc["B", "A"], 1.0, places=5)

        # Perfect negative correlation between A and C
        self.assertAlmostEqual(result.loc["A", "C"], -1.0, places=5)
        self.assertAlmostEqual(result.loc["C", "A"], -1.0, places=5)

        # Diagonal should be 1.0 (self-correlation)
        self.assertEqual(result.loc["A", "A"], 1.0)
        self.assertEqual(result.loc["B", "B"], 1.0)
        self.assertEqual(result.loc["C", "C"], 1.0)
        self.assertEqual(result.loc["D", "D"], 1.0)

    def test_corr_pearson_explicit(self):
        """Test correlation with explicit Pearson method."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._method_pin, "pearson")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        # Should be same as default
        self.assertAlmostEqual(result.loc["A", "B"], 1.0, places=5)
        self.assertAlmostEqual(result.loc["A", "C"], -1.0, places=5)

    def test_corr_spearman(self):
        """Test correlation with Spearman method."""
        # Create data where Spearman and Pearson might differ
        df_nonlinear = pd.DataFrame(
            {
                "A": [1, 2, 3, 4, 5],
                "B": [1, 4, 9, 16, 25],  # Quadratic relationship
            }
        )

        self.record.set(self.node._dataframe_pin, df_nonlinear)
        self.record.set(self.node._method_pin, "spearman")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        # Spearman should show perfect correlation for monotonic relationship
        self.assertAlmostEqual(result.loc["A", "B"], 1.0, places=5)

    def test_corr_kendall(self):
        """Test correlation with Kendall method."""
        simple_df = pd.DataFrame({"X": [1, 2, 3, 4, 5], "Y": [1, 2, 3, 4, 5]})

        self.record.set(self.node._dataframe_pin, simple_df)
        self.record.set(self.node._method_pin, "kendall")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        # Perfect monotonic relationship should give correlation of 1
        self.assertAlmostEqual(result.loc["X", "Y"], 1.0, places=5)

    def test_corr_with_na_values(self):
        """Test correlation with NaN values."""
        df_with_na = pd.DataFrame(
            {"A": [1, 2, None, 4, 5], "B": [2, 4, 6, None, 10], "C": [1, 2, 3, 4, 5]}
        )

        self.record.set(self.node._dataframe_pin, df_with_na)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        # Should still calculate correlations, ignoring NaN values
        self.assertFalse(pd.isna(result.loc["A", "C"]))
        self.assertFalse(pd.isna(result.loc["B", "C"]))

    def test_corr_min_periods(self):
        """Test correlation with min_periods parameter."""
        df_sparse = pd.DataFrame(
            {"A": [1, None, None, None, 5], "B": [None, None, 3, 4, None]}
        )

        # With min_periods=2, should require at least 2 valid pairs
        self.record.set(self.node._dataframe_pin, df_sparse)
        self.record.set(self.node._min_periods_pin, 2)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        # Correlation between A and B might be NaN due to insufficient pairs
        # The exact result depends on how many valid pairs exist

    def test_corr_single_column(self):
        """Test correlation with single column."""
        single_col_df = pd.DataFrame({"A": [1, 2, 3, 4, 5]})

        self.record.set(self.node._dataframe_pin, single_col_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (1, 1))
        self.assertEqual(result.loc["A", "A"], 1.0)

    def test_corr_constant_values(self):
        """Test correlation with constant values."""
        constant_df = pd.DataFrame(
            {
                "A": [1, 1, 1, 1, 1],  # Constant values
                "B": [2, 3, 4, 5, 6],
                "C": [3, 3, 3, 3, 3],  # Another constant
            }
        )

        self.record.set(self.node._dataframe_pin, constant_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        # Correlation with constant should be NaN
        self.assertTrue(pd.isna(result.loc["A", "B"]))
        self.assertTrue(pd.isna(result.loc["A", "C"]))
        self.assertTrue(pd.isna(result.loc["B", "A"]))

    def test_corr_two_columns(self):
        """Test correlation with exactly two columns."""
        two_col_df = pd.DataFrame({"X": [1, 2, 3, 4, 5], "Y": [6, 7, 8, 9, 10]})

        self.record.set(self.node._dataframe_pin, two_col_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (2, 2))
        # Perfect positive correlation
        self.assertAlmostEqual(result.loc["X", "Y"], 1.0, places=5)

    def test_corr_mixed_data_types(self):
        """Test correlation with mixed numeric data types."""
        mixed_df = pd.DataFrame(
            {
                "integers": [1, 2, 3, 4, 5],
                "floats": [1.5, 2.5, 3.5, 4.5, 5.5],
                "booleans": [True, False, True, False, True],
            }
        )

        self.record.set(self.node._dataframe_pin, mixed_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (3, 3))
        # Should handle mixed types properly
        self.assertAlmostEqual(result.loc["integers", "floats"], 1.0, places=5)

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_dataframe_pin"))
        self.assertTrue(hasattr(self.node, "_method_pin"))
        self.assertTrue(hasattr(self.node, "_min_periods_pin"))
        self.assertTrue(hasattr(self.node, "_output"))

        self.assertEqual(self.node._method_pin.name.value, "method")
        self.assertEqual(self.node._min_periods_pin.name.value, "min_periods")

        self.assertTrue(self.node._dataframe_pin.required)
        self.assertFalse(self.node._method_pin.required)
        self.assertFalse(self.node._min_periods_pin.required)


if __name__ == "__main__":
    main()
