# -*- coding: utf-8 -*-

from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas.manipulation.drop_node import DropNode
from cvp.nodes.record import NodeRecord


class DropNodeTestCase(TestCase):
    def setUp(self):
        self.node = DropNode()
        self.record = NodeRecord.empty()
        self.test_df = pd.DataFrame(
            {
                "A": [1, 2, 3, 4],
                "B": [5, 6, 7, 8],
                "C": [9, 10, 11, 12],
                "D": ["a", "b", "c", "d"],
            },
            index=["row1", "row2", "row3", "row4"],
        )

    def test_drop_single_column(self):
        """Test dropping a single column."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._additional_pins[0], "A")
        self.record.set(self.node._additional_pins[1], 1)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["B", "C", "D"])
        self.assertNotIn("A", result.columns)
        self.assertEqual(len(result), 4)

    def test_drop_multiple_columns(self):
        """Test dropping multiple columns."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._additional_pins[0], ["A", "C"])
        self.record.set(self.node._additional_pins[1], 1)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["B", "D"])
        self.assertNotIn("A", result.columns)
        self.assertNotIn("C", result.columns)

    def test_drop_single_row(self):
        """Test dropping a single row."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._additional_pins[0], "row1")
        self.record.set(self.node._additional_pins[1], 0)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.index), ["row2", "row3", "row4"])
        self.assertNotIn("row1", result.index)
        self.assertEqual(len(result), 3)

    def test_drop_multiple_rows(self):
        """Test dropping multiple rows."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._additional_pins[0], ["row1", "row3"])
        self.record.set(self.node._additional_pins[1], 0)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.index), ["row2", "row4"])
        self.assertEqual(len(result), 2)

    def test_drop_default_axis(self):
        """Test dropping with default axis (0 - rows)."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._additional_pins[0], "row2")
        # Don't set axis - should default to 0
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.index), ["row1", "row3", "row4"])
        self.assertNotIn("row2", result.index)

    def test_drop_with_integer_index(self):
        """Test dropping with integer index."""
        df_int_index = self.test_df.reset_index(drop=True)

        self.record.set(self.node._dataframe_pin, df_int_index)
        self.record.set(self.node._additional_pins[0], [0, 2])
        self.record.set(self.node._additional_pins[1], 0)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.index), [1, 3])
        self.assertEqual(len(result), 2)

    def test_drop_all_columns(self):
        """Test dropping all columns."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._additional_pins[0], ["A", "B", "C", "D"])
        self.record.set(self.node._additional_pins[1], 1)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result.columns), 0)
        self.assertEqual(len(result), 4)  # Rows still exist

    def test_drop_nonexistent_label(self):
        """Test dropping non-existent label."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._additional_pins[0], "nonexistent")
        self.record.set(self.node._additional_pins[1], 1)

        with self.assertRaises(KeyError):
            self.node.run(self.record)

    def test_drop_empty_dataframe(self):
        """Test dropping from empty DataFrame."""
        empty_df = pd.DataFrame()

        self.record.set(self.node._dataframe_pin, empty_df)
        self.record.set(self.node._additional_pins[0], [])
        self.record.set(self.node._additional_pins[1], 0)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_dataframe_pin"))
        self.assertTrue(hasattr(self.node, "_additional_pins"))
        self.assertTrue(hasattr(self.node, "_output"))
        self.assertEqual(len(self.node._additional_pins), 3)

        self.assertEqual(self.node._additional_pins[0].name, "labels")
        self.assertEqual(self.node._additional_pins[1].name, "axis")
        self.assertEqual(self.node._additional_pins[2].name, "inplace")

        self.assertFalse(self.node._dataframe_pin.required)
        self.assertFalse(self.node._additional_pins[0].required)
        self.assertFalse(self.node._additional_pins[1].required)
        self.assertFalse(self.node._additional_pins[2].required)


if __name__ == "__main__":
    main()
