# -*- coding: utf-8 -*-

from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas.manipulation.merge_node import MergeNode
from cvp.nodes.record import NodeRecord


class MergeNodeTestCase(TestCase):
    def setUp(self):
        self.node = MergeNode()
        self.record = NodeRecord.empty()
        self.left_df = pd.DataFrame({
            "key": ["A", "B", "C"],
            "left_value": [1, 2, 3]
        })
        self.right_df = pd.DataFrame({
            "key": ["A", "B", "D"],
            "right_value": [10, 20, 30]
        })

    def test_merge_inner_default(self):
        """Test inner merge (default behavior)."""
        self.record.set(self.node._left_pin, self.left_df)
        self.record.set(self.node._right_pin, self.right_df)
        self.record.set(self.node._on_pin, "key")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)  # Only A and B match
        self.assertEqual(list(result.columns), ["key", "left_value", "right_value"])
        self.assertEqual(result["key"].tolist(), ["A", "B"])
        self.assertEqual(result["left_value"].tolist(), [1, 2])
        self.assertEqual(result["right_value"].tolist(), [10, 20])

    def test_merge_left(self):
        """Test left merge."""
        self.record.set(self.node._left_pin, self.left_df)
        self.record.set(self.node._right_pin, self.right_df)
        self.record.set(self.node._on_pin, "key")
        self.record.set(self.node._how_pin, "left")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)  # All left records preserved
        self.assertEqual(result["key"].tolist(), ["A", "B", "C"])
        self.assertEqual(result["left_value"].tolist(), [1, 2, 3])
        self.assertEqual(result["right_value"].tolist(), [10, 20, None])

    def test_merge_right(self):
        """Test right merge."""
        self.record.set(self.node._left_pin, self.left_df)
        self.record.set(self.node._right_pin, self.right_df)
        self.record.set(self.node._on_pin, "key")
        self.record.set(self.node._how_pin, "right")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)  # All right records preserved
        self.assertEqual(result["key"].tolist(), ["A", "B", "D"])
        self.assertEqual(result["right_value"].tolist(), [10, 20, 30])
        self.assertTrue(pd.isna(result.loc[result["key"] == "D", "left_value"].iloc[0]))

    def test_merge_outer(self):
        """Test outer merge."""
        self.record.set(self.node._left_pin, self.left_df)
        self.record.set(self.node._right_pin, self.right_df)
        self.record.set(self.node._on_pin, "key")
        self.record.set(self.node._how_pin, "outer")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 4)  # All records from both sides
        self.assertEqual(sorted(result["key"].tolist()), ["A", "B", "C", "D"])

    def test_merge_without_on(self):
        """Test merge without specifying 'on' parameter."""
        # Create DataFrames with common columns
        left = pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35]
        })
        right = pd.DataFrame({
            "id": [1, 2, 4],
            "salary": [50000, 60000, 70000]
        })

        self.record.set(self.node._left_pin, left)
        self.record.set(self.node._right_pin, right)
        # Don't set 'on' parameter - should merge on common columns
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)  # Only id 1 and 2 match
        self.assertIn("id", result.columns)
        self.assertIn("name", result.columns)
        self.assertIn("salary", result.columns)

    def test_merge_multiple_keys(self):
        """Test merge on multiple columns."""
        left = pd.DataFrame({
            "key1": ["A", "A", "B", "B"],
            "key2": [1, 2, 1, 2],
            "left_value": [10, 20, 30, 40]
        })
        right = pd.DataFrame({
            "key1": ["A", "A", "B", "C"],
            "key2": [1, 3, 1, 1],
            "right_value": [100, 200, 300, 400]
        })

        self.record.set(self.node._left_pin, left)
        self.record.set(self.node._right_pin, right)
        self.record.set(self.node._on_pin, ["key1", "key2"])
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)  # Only (A,1) and (B,1) match
        expected_matches = [(("A", 1), (10, 100)), (("B", 1), (30, 300))]
        for i, row in result.iterrows():
            key_pair = (row["key1"], row["key2"])
            value_pair = (row["left_value"], row["right_value"])
            self.assertIn((key_pair, value_pair), expected_matches)

    def test_merge_different_column_names(self):
        """Test merge with different column names."""
        left = pd.DataFrame({
            "left_key": ["A", "B", "C"],
            "left_value": [1, 2, 3]
        })
        right = pd.DataFrame({
            "right_key": ["A", "B", "D"],
            "right_value": [10, 20, 30]
        })

        # This should work with pandas.merge using left_on/right_on,
        # but our simplified node uses 'on' parameter
        # So let's test with same column names renamed
        right_renamed = right.rename(columns={"right_key": "left_key"})

        self.record.set(self.node._left_pin, left)
        self.record.set(self.node._right_pin, right_renamed)
        self.record.set(self.node._on_pin, "left_key")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_left_pin"))
        self.assertTrue(hasattr(self.node, "_right_pin"))
        self.assertTrue(hasattr(self.node, "_on_pin"))
        self.assertTrue(hasattr(self.node, "_how_pin"))
        self.assertTrue(hasattr(self.node, "_output"))

        self.assertEqual(self.node._left_pin.name.value, "left")
        self.assertEqual(self.node._right_pin.name.value, "right")
        self.assertEqual(self.node._on_pin.name.value, "on")
        self.assertEqual(self.node._how_pin.name.value, "how")

        self.assertTrue(self.node._left_pin.required)
        self.assertTrue(self.node._right_pin.required)
        self.assertFalse(self.node._on_pin.required)
        self.assertFalse(self.node._how_pin.required)


if __name__ == "__main__":
    main()