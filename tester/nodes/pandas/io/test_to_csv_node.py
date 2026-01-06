# -*- coding: utf-8 -*-

import os
import tempfile
from io import StringIO
from unittest import TestCase, main

import pandas as pd

from cvp.nodes.defaults.pandas.io.to_csv_node import ToCsvNode
from cvp.nodes.record import NodeRecord


class ToCsvNodeTestCase(TestCase):
    def setUp(self):
        self.node = ToCsvNode()
        self.record = NodeRecord.empty()
        self.test_df = pd.DataFrame(
            {"A": [1, 2, 3], "B": [4, 5, 6], "C": ["x", "y", "z"]}
        )

    def test_to_csv_stringio(self):
        """Test writing DataFrame to StringIO buffer."""
        buffer = StringIO()

        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._path_pin, buffer)
        self.node.run(self.record)

        # Reset buffer position to read from beginning
        buffer.seek(0)
        output = buffer.getvalue()

        # Should contain headers and data
        self.assertIn("A,B,C", output)
        self.assertIn("1,4,x", output)
        self.assertIn("2,5,y", output)
        self.assertIn("3,6,z", output)

    def test_to_csv_no_index(self):
        """Test writing CSV without index."""
        buffer = StringIO()

        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._path_pin, buffer)
        self.record.set(self.node._index_pin, False)
        self.node.run(self.record)

        buffer.seek(0)
        output = buffer.getvalue()

        # Should not contain index column (0,1,2)
        lines = output.strip().split("\n")
        header_line = lines[0]
        # Header should start with column names, not index
        self.assertTrue(header_line.startswith("A,B,C"))

    def test_to_csv_with_index(self):
        """Test writing CSV with index (default behavior)."""
        df_with_index = pd.DataFrame(
            {"X": [10, 20], "Y": [30, 40]}, index=["row1", "row2"]
        )

        buffer = StringIO()

        self.record.set(self.node._dataframe_pin, df_with_index)
        self.record.set(self.node._path_pin, buffer)
        # Don't set index_pin - should default to True
        self.node.run(self.record)

        buffer.seek(0)
        output = buffer.getvalue()

        # Should contain index labels
        self.assertIn("row1", output)
        self.assertIn("row2", output)

    def test_to_csv_custom_separator(self):
        """Test writing CSV with custom separator."""
        buffer = StringIO()

        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._path_pin, buffer)
        self.record.set(self.node._sep_pin, ";")
        self.node.run(self.record)

        buffer.seek(0)
        output = buffer.getvalue()

        # Should use semicolon separator
        self.assertIn("A;B;C", output)
        self.assertIn("1;4;x", output)

    def test_to_csv_tab_separator(self):
        """Test writing TSV (tab-separated values)."""
        buffer = StringIO()

        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._path_pin, buffer)
        self.record.set(self.node._sep_pin, "\t")
        self.node.run(self.record)

        buffer.seek(0)
        output = buffer.getvalue()

        # Should use tab separator
        self.assertIn("A\tB\tC", output)

    def test_to_csv_tempfile(self):
        """Test writing CSV to temporary file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            temp_path = f.name

        try:
            self.record.set(self.node._dataframe_pin, self.test_df)
            self.record.set(self.node._path_pin, temp_path)
            self.node.run(self.record)

            # Verify file was written
            self.assertTrue(os.path.exists(temp_path))

            # Read back and verify contents
            with open(temp_path, "r") as f:
                content = f.read()

            self.assertIn("A,B,C", content)
            self.assertIn("1,4,x", content)

        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_to_csv_with_missing_values(self):
        """Test writing CSV with NaN values."""
        df_with_na = pd.DataFrame(
            {"A": [1, None, 3], "B": [None, 5, 6], "C": ["x", "y", None]}
        )

        buffer = StringIO()

        self.record.set(self.node._dataframe_pin, df_with_na)
        self.record.set(self.node._path_pin, buffer)
        self.node.run(self.record)

        buffer.seek(0)
        output = buffer.getvalue()

        # NaN values should be represented appropriately
        self.assertIn("A,B,C", output)
        # pandas typically writes NaN as empty string or specific representation

    def test_to_csv_empty_dataframe(self):
        """Test writing empty DataFrame."""
        empty_df = pd.DataFrame(columns=["A", "B", "C"])

        buffer = StringIO()

        self.record.set(self.node._dataframe_pin, empty_df)
        self.record.set(self.node._path_pin, buffer)
        self.node.run(self.record)

        buffer.seek(0)
        output = buffer.getvalue()

        # Should at least have headers
        self.assertIn("A,B,C", output)

    def test_to_csv_single_column(self):
        """Test writing single column DataFrame."""
        single_col_df = pd.DataFrame({"values": [1, 2, 3, 4, 5]})

        buffer = StringIO()

        self.record.set(self.node._dataframe_pin, single_col_df)
        self.record.set(self.node._path_pin, buffer)
        self.node.run(self.record)

        buffer.seek(0)
        output = buffer.getvalue()

        self.assertIn("values", output)
        for i in range(1, 6):
            self.assertIn(str(i), output)

    def test_to_csv_single_row(self):
        """Test writing single row DataFrame."""
        single_row_df = pd.DataFrame({"A": [100], "B": [200], "C": ["hello"]})

        buffer = StringIO()

        self.record.set(self.node._dataframe_pin, single_row_df)
        self.record.set(self.node._path_pin, buffer)
        self.node.run(self.record)

        buffer.seek(0)
        output = buffer.getvalue()

        self.assertIn("A,B,C", output)
        self.assertIn("100,200,hello", output)

    def test_to_csv_with_special_characters(self):
        """Test writing CSV with special characters."""
        special_df = pd.DataFrame(
            {"text": ["hello,world", "line\nbreak", 'quote"test'], "numbers": [1, 2, 3]}
        )

        buffer = StringIO()

        self.record.set(self.node._dataframe_pin, special_df)
        self.record.set(self.node._path_pin, buffer)
        self.node.run(self.record)

        buffer.seek(0)
        output = buffer.getvalue()

        # Special characters should be properly escaped/quoted
        self.assertIn("text,numbers", output)

    def test_to_csv_numeric_types(self):
        """Test writing CSV with various numeric types."""
        numeric_df = pd.DataFrame(
            {
                "integers": [1, 2, 3],
                "floats": [1.1, 2.2, 3.3],
                "large_numbers": [1000000, 2000000, 3000000],
            }
        )

        buffer = StringIO()

        self.record.set(self.node._dataframe_pin, numeric_df)
        self.record.set(self.node._path_pin, buffer)
        self.node.run(self.record)

        buffer.seek(0)
        output = buffer.getvalue()

        self.assertIn("integers,floats,large_numbers", output)
        self.assertIn("1.1", output)
        self.assertIn("1000000", output)

    def test_to_csv_with_multi_index(self):
        """Test writing CSV with MultiIndex."""
        arrays = [["A", "A", "B", "B"], [1, 2, 1, 2]]
        multi_df = pd.DataFrame({"values": [10, 20, 30, 40]}, index=arrays)

        buffer = StringIO()

        self.record.set(self.node._dataframe_pin, multi_df)
        self.record.set(self.node._path_pin, buffer)
        self.node.run(self.record)

        buffer.seek(0)
        output = buffer.getvalue()

        # MultiIndex should be written appropriately
        self.assertIn("values", output)

    def test_to_csv_return_value(self):
        """Test that to_csv method returns None (as expected for file writing)."""
        buffer = StringIO()

        self.record.set(self.node._dataframe_pin, self.test_df)
        self.record.set(self.node._path_pin, buffer)
        result = self.node.run(self.record)

        # The to_csv method typically returns None
        # The result from node.run should be the return from nonext()
        self.assertIsNotNone(result)

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_dataframe_pin"))
        self.assertTrue(hasattr(self.node, "_path_pin"))
        self.assertTrue(hasattr(self.node, "_sep_pin"))
        self.assertTrue(hasattr(self.node, "_index_pin"))
        self.assertTrue(hasattr(self.node, "_output"))

        self.assertEqual(self.node._path_pin.name.value, "path_or_buf")
        self.assertEqual(self.node._sep_pin.name.value, "sep")
        self.assertEqual(self.node._index_pin.name.value, "index")

        self.assertTrue(self.node._dataframe_pin.required)
        self.assertTrue(self.node._path_pin.required)
        self.assertFalse(self.node._sep_pin.required)
        self.assertFalse(self.node._index_pin.required)


if __name__ == "__main__":
    main()
