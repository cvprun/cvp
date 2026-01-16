# -*- coding: utf-8 -*-

import json
import os
import tempfile
from io import StringIO
from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas.io.read_json_node import ReadJsonNode
from cvp.nodes.record import NodeRecord


class ReadJsonNodeTestCase(TestCase):
    def setUp(self):
        self.node = ReadJsonNode()
        self.record = NodeRecord.empty()

    def test_read_json_from_stringio(self):
        """Test reading JSON from StringIO buffer."""
        json_data = '{"A": [1, 4, 7], "B": [2, 5, 8], "C": [3, 6, 9]}'
        buffer = StringIO(json_data)

        self.record.set(self.node._path_pin, buffer)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B", "C"])
        self.assertEqual(len(result), 3)
        self.assertEqual(result["A"].tolist(), [1, 4, 7])
        self.assertEqual(result["B"].tolist(), [2, 5, 8])
        self.assertEqual(result["C"].tolist(), [3, 6, 9])

    def test_read_json_orient_records(self):
        """Test reading JSON with 'records' orientation."""
        json_data = '[{"A": 1, "B": 2}, {"A": 3, "B": 4}, {"A": 5, "B": 6}]'
        buffer = StringIO(json_data)

        self.record.set(self.node._path_pin, buffer)
        self.record.set(self.node._orient_pin, "records")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B"])
        self.assertEqual(len(result), 3)
        self.assertEqual(result["A"].tolist(), [1, 3, 5])
        self.assertEqual(result["B"].tolist(), [2, 4, 6])

    def test_read_json_orient_index(self):
        """Test reading JSON with 'index' orientation."""
        json_data = '{"row1": {"A": 1, "B": 2}, "row2": {"A": 3, "B": 4}}'
        buffer = StringIO(json_data)

        self.record.set(self.node._path_pin, buffer)
        self.record.set(self.node._orient_pin, "index")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B"])
        self.assertEqual(list(result.index), ["row1", "row2"])
        self.assertEqual(result.loc["row1", "A"], 1)
        self.assertEqual(result.loc["row2", "B"], 4)

    def test_read_json_orient_values(self):
        """Test reading JSON with 'values' orientation."""
        json_data = "[[1, 2], [3, 4], [5, 6]]"
        buffer = StringIO(json_data)

        self.record.set(self.node._path_pin, buffer)
        self.record.set(self.node._orient_pin, "values")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)
        self.assertEqual(len(result.columns), 2)
        self.assertEqual(result.iloc[0, 0], 1)
        self.assertEqual(result.iloc[2, 1], 6)

    def test_read_json_orient_columns(self):
        """Test reading JSON with 'columns' orientation."""
        json_data = '{"A": {"0": 1, "1": 3}, "B": {"0": 2, "1": 4}}'
        buffer = StringIO(json_data)

        self.record.set(self.node._path_pin, buffer)
        self.record.set(self.node._orient_pin, "columns")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B"])
        self.assertEqual(len(result), 2)

    def test_read_json_from_tempfile(self):
        """Test reading JSON from temporary file."""
        data = {"X": [10, 40], "Y": [20, 50], "Z": [30, 60]}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            temp_path = f.name

        try:
            self.record.set(self.node._path_pin, temp_path)
            self.node.run(self.record)
            result = self.record.get(self.node._output)

            self.assertIsInstance(result, pd.DataFrame)
            self.assertEqual(list(result.columns), ["X", "Y", "Z"])
            self.assertEqual(len(result), 2)
            self.assertEqual(result["X"].tolist(), [10, 40])
        finally:
            os.unlink(temp_path)

    def test_read_json_nested_data(self):
        """Test reading JSON with nested data."""
        json_data = """[
            {"name": "Alice", "age": 25, "address": {"city": "NYC", "state": "NY"}},
            {"name": "Bob", "age": 30, "address": {"city": "LA", "state": "CA"}}
        ]"""
        buffer = StringIO(json_data)

        self.record.set(self.node._path_pin, buffer)
        self.record.set(self.node._orient_pin, "records")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("name", result.columns)
        self.assertIn("age", result.columns)
        self.assertIn("address", result.columns)
        self.assertEqual(result["name"].tolist(), ["Alice", "Bob"])

    def test_read_json_with_null_values(self):
        """Test reading JSON with null values."""
        json_data = '{"A": [1, null, 3], "B": [null, 2, null]}'
        buffer = StringIO(json_data)

        self.record.set(self.node._path_pin, buffer)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)
        self.assertTrue(pd.isna(result["A"].iloc[1]))
        self.assertTrue(pd.isna(result["B"].iloc[0]))
        self.assertTrue(pd.isna(result["B"].iloc[2]))

    def test_read_json_mixed_types(self):
        """Test reading JSON with mixed data types."""
        json_data = """[
            {"str": "hello", "int": 1, "float": 1.5, "bool": true},
            {"str": "world", "int": 2, "float": 2.7, "bool": false}
        ]"""
        buffer = StringIO(json_data)

        self.record.set(self.node._path_pin, buffer)
        self.record.set(self.node._orient_pin, "records")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertEqual(result["str"].tolist(), ["hello", "world"])
        self.assertEqual(result["int"].tolist(), [1, 2])
        self.assertEqual(result["bool"].tolist(), [True, False])

    def test_read_json_empty_object(self):
        """Test reading empty JSON object."""
        json_data = "{}"
        buffer = StringIO(json_data)

        self.record.set(self.node._path_pin, buffer)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)

    def test_read_json_empty_array(self):
        """Test reading empty JSON array."""
        json_data = "[]"
        buffer = StringIO(json_data)

        self.record.set(self.node._path_pin, buffer)
        self.record.set(self.node._orient_pin, "records")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)

    def test_read_json_single_record(self):
        """Test reading JSON with single record."""
        json_data = '{"A": 1, "B": 2, "C": 3}'
        buffer = StringIO(json_data)

        self.record.set(self.node._path_pin, buffer)
        self.record.set(self.node._orient_pin, "series")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        # When reading with series orientation, pandas might return a Series
        # Convert to DataFrame for consistency if needed
        if isinstance(result, pd.Series):
            result = result.to_frame().T

        self.assertIsInstance(result, (pd.DataFrame, pd.Series))

    def test_read_json_large_numbers(self):
        """Test reading JSON with large numbers."""
        json_data = (
            '{"large_int": [1000000000, 2000000000], "large_float": [1.23e10, 4.56e15]}'
        )
        buffer = StringIO(json_data)

        self.record.set(self.node._path_pin, buffer)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertEqual(result["large_int"].iloc[0], 1000000000)

    def test_read_json_date_strings(self):
        """Test reading JSON with date strings."""
        json_data = '{"date": ["2023-01-01", "2023-12-31"], "value": [100, 200]}'
        buffer = StringIO(json_data)

        self.record.set(self.node._path_pin, buffer)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertEqual(result["date"].tolist(), ["2023-01-01", "2023-12-31"])

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_path_pin"))
        self.assertTrue(hasattr(self.node, "_orient_pin"))
        self.assertTrue(hasattr(self.node, "_output"))

        self.assertEqual(self.node._path_pin.name.value, "path_or_buf")
        self.assertEqual(self.node._orient_pin.name.value, "orient")

        self.assertTrue(self.node._path_pin.required)
        self.assertFalse(self.node._orient_pin.required)


if __name__ == "__main__":
    main()
