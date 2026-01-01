# -*- coding: utf-8 -*-

from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas.statistics.mean_node import MeanNode
from cvp.nodes.record import NodeRecord


class MeanNodeTestCase(TestCase):
    def setUp(self):
        self.node = MeanNode()
        self.record = NodeRecord.empty()
        self.test_df = pd.DataFrame({
            "A": [1, 2, 3, 4],
            "B": [10, 20, 30, 40],
            "C": [1.5, 2.5, 3.5, 4.5]
        })

    def test_mean_default(self):
        """Test mean calculation with default settings."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result["A"], 2.5)  # (1+2+3+4)/4
        self.assertEqual(result["B"], 25.0)  # (10+20+30+40)/4
        self.assertEqual(result["C"], 3.0)   # (1.5+2.5+3.5+4.5)/4

    def test_mean_axis_0(self):
        """Test mean calculation along axis 0 (rows)."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._additional_pins[0], 0)  # axis pin
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result["A"], 2.5)
        self.assertEqual(result["B"], 25.0)
        self.assertEqual(result["C"], 3.0)

    def test_mean_axis_1(self):
        """Test mean calculation along axis 1 (columns)."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._additional_pins[0], 1)  # axis pin
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), 4)  # One mean per row
        # Row 0: (1+10+1.5)/3 = 4.17
        self.assertAlmostEqual(result[0], 4.166666666666667, places=5)
        # Row 1: (2+20+2.5)/3 = 8.17
        self.assertAlmostEqual(result[1], 8.166666666666666, places=5)

    def test_mean_with_na_values(self):
        """Test mean calculation with NaN values."""
        df_with_na = pd.DataFrame({
            "A": [1, 2, None, 4],
            "B": [10, None, 30, 40],
            "C": [1.0, 2.0, 3.0, 4.0]
        })

        self.record.set(self.node._dataframe_pin, df_with_na)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        # A: (1+2+4)/3 = 2.33 (ignoring NaN by default)
        self.assertAlmostEqual(result["A"], 2.3333333333333335, places=5)
        # B: (10+30+40)/3 = 26.67
        self.assertAlmostEqual(result["B"], 26.666666666666668, places=5)
        # C: (1+2+3+4)/4 = 2.5
        self.assertEqual(result["C"], 2.5)

    def test_mean_skipna_false(self):
        """Test mean calculation without skipping NaN values."""
        df_with_na = pd.DataFrame({
            "A": [1, 2, None, 4],
            "B": [10, 20, 30, 40]
        })

        self.record.set(self.node._dataframe_pin, df_with_na)
        self.record.set(self.node._additional_pins[1], False)  # skipna pin
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        # A should be NaN because it contains NaN
        self.assertTrue(pd.isna(result["A"]))
        # B should still be valid
        self.assertEqual(result["B"], 25.0)

    def test_mean_empty_dataframe(self):
        """Test mean calculation on empty DataFrame."""
        empty_df = pd.DataFrame()

        self.record.set(self.node._dataframe_pin, empty_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertTrue(result.empty)

    def test_mean_single_row(self):
        """Test mean calculation on single row DataFrame."""
        single_row_df = pd.DataFrame({"A": [5], "B": [15], "C": [25]})

        self.record.set(self.node._dataframe_pin, single_row_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result["A"], 5.0)
        self.assertEqual(result["B"], 15.0)
        self.assertEqual(result["C"], 25.0)

    def test_mean_single_column(self):
        """Test mean calculation on single column DataFrame."""
        single_col_df = pd.DataFrame({"A": [1, 2, 3, 4, 5]})

        self.record.set(self.node._dataframe_pin, single_col_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result["A"], 3.0)

    def test_mean_mixed_types(self):
        """Test mean calculation with mixed numeric types."""
        mixed_df = pd.DataFrame({
            "integers": [1, 2, 3, 4],
            "floats": [1.1, 2.2, 3.3, 4.4],
            "booleans": [True, False, True, False]  # Should be treated as 1, 0, 1, 0
        })

        self.record.set(self.node._dataframe_pin, mixed_df)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result["integers"], 2.5)
        self.assertAlmostEqual(result["floats"], 2.75, places=5)
        self.assertEqual(result["booleans"], 0.5)  # (1+0+1+0)/4

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_dataframe_pin"))
        self.assertTrue(hasattr(self.node, "_additional_pins"))
        self.assertTrue(hasattr(self.node, "_output"))

        # Should have 2 additional pins: axis, skipna
        self.assertEqual(len(self.node._additional_pins), 2)

        self.assertEqual(self.node._additional_pins[0].name, "axis")
        self.assertEqual(self.node._additional_pins[1].name, "skipna")

        self.assertTrue(self.node._dataframe_pin.required)
        self.assertFalse(self.node._additional_pins[0].required)  # axis pin
        self.assertFalse(self.node._additional_pins[1].required)  # skipna pin


if __name__ == "__main__":
    main()