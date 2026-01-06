# -*- coding: utf-8 -*-

from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas.manipulation.sort_values_node import SortValuesNode
from cvp.nodes.record import NodeRecord


class SortValuesNodeTestCase(TestCase):
    def setUp(self):
        self.node = SortValuesNode()
        self.record = NodeRecord.empty()
        self.test_df = pd.DataFrame(
            {"A": [3, 1, 4, 2], "B": [30, 10, 40, 20], "C": ["c", "a", "d", "b"]}
        )

    def test_sort_by_single_column(self):
        """Test sorting by single column."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._additional_pins[0], "A")  # by pin
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result["A"].tolist(), [1, 2, 3, 4])
        self.assertEqual(result["B"].tolist(), [10, 20, 30, 40])
        self.assertEqual(result["C"].tolist(), ["a", "b", "c", "d"])

    def test_sort_by_multiple_columns(self):
        """Test sorting by multiple columns."""
        test_df = pd.DataFrame(
            {"A": [1, 2, 1, 2], "B": [4, 3, 2, 1], "C": ["d", "c", "b", "a"]}
        )

        self.record.set(self.node._dataframe_pin, test_df)
        self.record.set(self.node._additional_pins[0], ["A", "B"])  # by pin
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        # Should sort by A first, then B within each A group
        expected = pd.DataFrame(
            {"A": [1, 1, 2, 2], "B": [2, 4, 1, 3], "C": ["b", "d", "a", "c"]},
            index=[2, 0, 3, 1],
        )

        pd.testing.assert_frame_equal(
            result.reset_index(drop=True), expected.reset_index(drop=True)
        )

    def test_sort_descending(self):
        """Test sorting in descending order."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._additional_pins[0], "A")  # by pin
        self.record.set(self.node._additional_pins[1], False)  # ascending pin
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result["A"].tolist(), [4, 3, 2, 1])
        self.assertEqual(result["B"].tolist(), [40, 30, 20, 10])

    def test_sort_mixed_ascending(self):
        """Test sorting with mixed ascending/descending."""
        test_df = pd.DataFrame(
            {
                "A": [1, 2, 1, 2],
                "B": [4, 3, 2, 1],
            }
        )

        self.record.set(self.node._dataframe_pin, test_df)
        self.record.set(self.node._additional_pins[0], ["A", "B"])  # by pin
        self.record.set(self.node._additional_pins[1], [True, False])  # ascending pin
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        # A ascending, B descending
        expected_A = [1, 1, 2, 2]
        expected_B = [4, 2, 3, 1]
        self.assertEqual(result["A"].tolist(), expected_A)
        self.assertEqual(result["B"].tolist(), expected_B)

    def test_sort_string_column(self):
        """Test sorting string column."""
        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._additional_pins[0], "C")  # by pin
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result["C"].tolist(), ["a", "b", "c", "d"])
        self.assertEqual(result["A"].tolist(), [1, 2, 3, 4])

    def test_sort_with_na_values(self):
        """Test sorting with NA values."""
        test_df = pd.DataFrame({"A": [3, None, 1, 2], "B": [30, 50, 10, 20]})

        self.record.set(self.node._dataframe_pin, test_df)
        self.record.set(self.node._additional_pins[0], "A")  # by pin
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        # NA values should be at the end by default
        self.assertEqual(len(result), 4)
        self.assertFalse(pd.isna(result["A"].iloc[0]))  # First non-NA value

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_dataframe_pin"))
        self.assertTrue(hasattr(self.node, "_additional_pins"))
        self.assertTrue(hasattr(self.node, "_output"))

        # Should have 3 additional pins: by, ascending, inplace
        self.assertEqual(len(self.node._additional_pins), 3)

        # Check pin names
        self.assertEqual(self.node._additional_pins[0].name.value, "by")
        self.assertEqual(self.node._additional_pins[1].name.value, "ascending")
        self.assertEqual(self.node._additional_pins[2].name.value, "inplace")

        self.assertTrue(self.node._dataframe_pin.required)
        self.assertTrue(self.node._additional_pins[0].required)  # by pin
        self.assertFalse(self.node._additional_pins[1].required)  # ascending pin
        self.assertFalse(self.node._additional_pins[2].required)  # inplace pin


if __name__ == "__main__":
    main()
