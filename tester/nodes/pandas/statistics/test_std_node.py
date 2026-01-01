# -*- coding: utf-8 -*-

from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas.statistics.std_node import StdNode
from cvp.nodes.record import NodeRecord


class StdNodeTestCase(TestCase):
    def setUp(self):
        self.node = StdNode()
        self.record = NodeRecord.empty()
        self.test_df = pd.DataFrame({
            "A": [1, 2, 3, 4, 5],
            "B": [10, 20, 30, 40, 50],
            "C": [1.0, 1.0, 1.0, 1.0, 1.0]  # Zero variance
        })

    def test_std_default(self):
        """Test standard deviation calculation with default settings."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        # A: std([1,2,3,4,5]) with ddof=1
        expected_std_a = pd.Series([1, 2, 3, 4, 5]).std()
        self.assertAlmostEqual(result["A"], expected_std_a, places=5)

        # B: std([10,20,30,40,50]) with ddof=1
        expected_std_b = pd.Series([10, 20, 30, 40, 50]).std()
        self.assertAlmostEqual(result["B"], expected_std_b, places=5)

        # C: std of constant values should be 0
        self.assertEqual(result["C"], 0.0)

    def test_std_axis_0(self):
        """Test std calculation along axis 0 (rows)."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._axis_pin, 0)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), 3)  # One std per column

    def test_std_axis_1(self):
        """Test std calculation along axis 1 (columns)."""
        test_df = pd.DataFrame({
            "A": [1, 4, 7],
            "B": [2, 5, 8],
            "C": [3, 6, 9]
        })

        self.record.set(self.node._dataframe_pin, test_df)
        self.record.set(self.node._axis_pin, 1)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), 3)  # One std per row
        # Row 0: std([1,2,3])
        expected_std_row0 = pd.Series([1, 2, 3]).std()
        self.assertAlmostEqual(result[0], expected_std_row0, places=5)

    def test_std_ddof_0(self):
        """Test std calculation with ddof=0 (population std)."""
        simple_df = pd.DataFrame({"A": [1, 2, 3, 4, 5]})

        self.record.set(self.node._dataframe_pin, simple_df)
        self.record.set(self.node._ddof_pin, 0)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        # Population std (ddof=0) should be different from sample std (ddof=1)
        expected_std = pd.Series([1, 2, 3, 4, 5]).std(ddof=0)
        self.assertAlmostEqual(result["A"], expected_std, places=5)

    def test_std_with_na_values(self):
        """Test std calculation with NaN values."""
        df_with_na = pd.DataFrame({
            "A": [1, 2, None, 4, 5],
            "B": [10, None, 30, None, 50],
            "C": [1.0, 2.0, 3.0, 4.0, 5.0]
        })

        self.record.set(self.node._dataframe_pin, df_with_na)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        # A: std([1,2,4,5]) ignoring NaN
        expected_std_a = pd.Series([1, 2, 4, 5]).std()
        self.assertAlmostEqual(result["A"], expected_std_a, places=5)

        # B: std([10,30,50]) ignoring NaN
        expected_std_b = pd.Series([10, 30, 50]).std()
        self.assertAlmostEqual(result["B"], expected_std_b, places=5)

    def test_std_skipna_false(self):
        """Test std calculation without skipping NaN values."""
        df_with_na = pd.DataFrame({
            "A": [1, 2, None, 4],
            "B": [10, 20, 30, 40]
        })

        self.record.set(self.node._dataframe_pin, df_with_na)
        self.record.set(self.node._skipna_pin, False)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        # A should be NaN because it contains NaN and skipna=False
        self.assertTrue(pd.isna(result["A"]))
        # B should still be valid
        expected_std_b = pd.Series([10, 20, 30, 40]).std()
        self.assertAlmostEqual(result["B"], expected_std_b, places=5)

    def test_std_single_value(self):
        """Test std calculation with single value."""
        single_df = pd.DataFrame({"A": [5]})

        self.record.set(self.node._dataframe_pin, single_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        # Standard deviation of a single value is NaN with ddof=1
        self.assertTrue(pd.isna(result["A"]))

    def test_std_single_value_ddof_0(self):
        """Test std calculation with single value and ddof=0."""
        single_df = pd.DataFrame({"A": [5]})

        self.record.set(self.node._dataframe_pin, single_df)
        self.record.set(self.node._ddof_pin, 0)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        # Standard deviation of a single value with ddof=0 is 0
        self.assertEqual(result["A"], 0.0)

    def test_std_two_values(self):
        """Test std calculation with two values."""
        two_val_df = pd.DataFrame({"A": [1, 3]})

        self.record.set(self.node._dataframe_pin, two_val_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        expected_std = pd.Series([1, 3]).std()
        self.assertAlmostEqual(result["A"], expected_std, places=5)

    def test_std_empty_dataframe(self):
        """Test std calculation on empty DataFrame."""
        empty_df = pd.DataFrame()

        self.record.set(self.node._dataframe_pin, empty_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertTrue(result.empty)

    def test_std_large_values(self):
        """Test std calculation with large values."""
        large_df = pd.DataFrame({
            "A": [1000000, 2000000, 3000000, 4000000, 5000000]
        })

        self.record.set(self.node._dataframe_pin, large_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        expected_std = pd.Series([1000000, 2000000, 3000000, 4000000, 5000000]).std()
        self.assertAlmostEqual(result["A"], expected_std, places=0)

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_dataframe_pin"))
        self.assertTrue(hasattr(self.node, "_axis_pin"))
        self.assertTrue(hasattr(self.node, "_skipna_pin"))
        self.assertTrue(hasattr(self.node, "_ddof_pin"))
        self.assertTrue(hasattr(self.node, "_output"))

        self.assertEqual(self.node._axis_pin.name.value, "axis")
        self.assertEqual(self.node._skipna_pin.name.value, "skipna")
        self.assertEqual(self.node._ddof_pin.name.value, "ddof")

        self.assertTrue(self.node._dataframe_pin.required)
        self.assertFalse(self.node._axis_pin.required)
        self.assertFalse(self.node._skipna_pin.required)
        self.assertFalse(self.node._ddof_pin.required)


if __name__ == "__main__":
    main()