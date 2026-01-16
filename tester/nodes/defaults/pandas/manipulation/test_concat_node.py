# -*- coding: utf-8 -*-

from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas.manipulation.concat_node import ConcatNode
from cvp.nodes.record import NodeRecord


class ConcatNodeTestCase(TestCase):
    def setUp(self):
        self.node = ConcatNode()
        self.record = NodeRecord.empty()
        self.df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        self.df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]})
        self.df3 = pd.DataFrame({"C": [9, 10], "D": [11, 12]})

    def test_concat_dataframes_default(self):
        """Test concatenating DataFrames with default settings."""
        self.record.set(self.node._objs_pin, [self.df1, self.df2])
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B"])
        self.assertEqual(len(result), 4)
        self.assertEqual(result["A"].tolist(), [1, 2, 5, 6])
        self.assertEqual(result["B"].tolist(), [3, 4, 7, 8])

    def test_concat_with_ignore_index(self):
        """Test concatenation with ignore_index=True."""
        self.record.set(self.node._objs_pin, [self.df1, self.df2])
        self.record.set(self.node._ignore_index_pin, True)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.index), [0, 1, 2, 3])
        self.assertEqual(result["A"].tolist(), [1, 2, 5, 6])

    def test_concat_axis_1(self):
        """Test concatenation along axis 1 (columns)."""
        self.record.set(self.node._objs_pin, [self.df1, self.df3])
        self.record.set(self.node._axis_pin, 1)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B", "C", "D"])
        self.assertEqual(len(result), 2)
        self.assertEqual(result["A"].tolist(), [1, 2])
        self.assertEqual(result["C"].tolist(), [9, 10])

    def test_concat_series(self):
        """Test concatenating Series."""
        s1 = pd.Series([1, 2, 3], name="series1")
        s2 = pd.Series([4, 5, 6], name="series2")

        self.record.set(self.node._objs_pin, [s1, s2])
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), 6)
        self.assertEqual(result.tolist(), [1, 2, 3, 4, 5, 6])

    def test_concat_series_axis_1(self):
        """Test concatenating Series along axis 1."""
        s1 = pd.Series([1, 2, 3], name="series1")
        s2 = pd.Series([4, 5, 6], name="series2")

        self.record.set(self.node._objs_pin, [s1, s2])
        self.record.set(self.node._axis_pin, 1)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["series1", "series2"])
        self.assertEqual(len(result), 3)

    def test_concat_different_columns(self):
        """Test concatenating DataFrames with different columns."""
        df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        df2 = pd.DataFrame({"A": [5, 6], "C": [7, 8]})

        self.record.set(self.node._objs_pin, [df1, df2])
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(sorted(result.columns), ["A", "B", "C"])
        self.assertEqual(len(result), 4)
        # B column should have NaN for second dataframe
        self.assertTrue(pd.isna(result.loc[2, "B"]))
        # C column should have NaN for first dataframe
        self.assertTrue(pd.isna(result.loc[0, "C"]))

    def test_concat_empty_list(self):
        """Test concatenating empty list."""
        self.record.set(self.node._objs_pin, [])
        try:
            self.node.run(self.record)
            result = self.record.get(self.node._output)
            # If it doesn't raise an error, result should be empty
            if result is not None:
                self.assertTrue(result.empty or len(result) == 0)
        except (ValueError, TypeError):
            # pandas.concat with empty list should raise an error
            pass

    def test_concat_single_object(self):
        """Test concatenating single object."""
        self.record.set(self.node._objs_pin, [self.df1])
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        pd.testing.assert_frame_equal(result, self.df1)

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_objs_pin"))
        self.assertTrue(hasattr(self.node, "_axis_pin"))
        self.assertTrue(hasattr(self.node, "_ignore_index_pin"))
        self.assertTrue(hasattr(self.node, "_output"))

        self.assertEqual(self.node._objs_pin.name.value, "objs")
        self.assertEqual(self.node._axis_pin.name.value, "axis")
        self.assertEqual(self.node._ignore_index_pin.name.value, "ignore_index")

        self.assertTrue(self.node._objs_pin.required)
        self.assertFalse(self.node._axis_pin.required)
        self.assertFalse(self.node._ignore_index_pin.required)


if __name__ == "__main__":
    main()
