# -*- coding: utf-8 -*-

from unittest import TestCase, main
import tempfile
import os
from io import StringIO

import pandas as pd

from cvp.nodes.defaults.pandas.io.read_csv_node import ReadCsvNode
from cvp.nodes.record import NodeRecord


class ReadCsvNodeTestCase(TestCase):
    def setUp(self):
        self.node = ReadCsvNode()
        self.record = NodeRecord.empty()

    def test_read_csv_from_stringio(self):
        """Test reading CSV from StringIO buffer."""
        csv_data = "A,B,C\n1,2,3\n4,5,6\n7,8,9"
        buffer = StringIO(csv_data)

        self.record.set(self.node._filepath_pin, buffer)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B", "C"])
        self.assertEqual(len(result), 3)
        self.assertEqual(result["A"].tolist(), [1, 4, 7])
        self.assertEqual(result["B"].tolist(), [2, 5, 8])
        self.assertEqual(result["C"].tolist(), [3, 6, 9])

    def test_read_csv_with_custom_separator(self):
        """Test reading CSV with custom separator."""
        csv_data = "A;B;C\n1;2;3\n4;5;6"
        buffer = StringIO(csv_data)

        self.record.set(self.node._filepath_pin, buffer)
        self.record.set(self.node._sep_pin, ";")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B", "C"])
        self.assertEqual(len(result), 2)

    def test_read_csv_no_header(self):
        """Test reading CSV without header."""
        csv_data = "1,2,3\n4,5,6\n7,8,9"
        buffer = StringIO(csv_data)

        self.record.set(self.node._filepath_pin, buffer)
        self.record.set(self.node._header_pin, None)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        # Should have default column names (0, 1, 2)
        self.assertEqual(list(result.columns), [0, 1, 2])
        self.assertEqual(len(result), 3)

    def test_read_csv_with_index_column(self):
        """Test reading CSV with index column."""
        csv_data = "index,A,B,C\nrow1,1,2,3\nrow2,4,5,6\nrow3,7,8,9"
        buffer = StringIO(csv_data)

        self.record.set(self.node._filepath_pin, buffer)
        self.record.set(self.node._index_col_pin, 0)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B", "C"])
        self.assertEqual(list(result.index), ["row1", "row2", "row3"])

    def test_read_csv_with_named_index_column(self):
        """Test reading CSV with named index column."""
        csv_data = "name,A,B,C\nrow1,1,2,3\nrow2,4,5,6"
        buffer = StringIO(csv_data)

        self.record.set(self.node._filepath_pin, buffer)
        self.record.set(self.node._index_col_pin, "name")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B", "C"])
        self.assertEqual(list(result.index), ["row1", "row2"])

    def test_read_csv_from_tempfile(self):
        """Test reading CSV from temporary file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("X,Y,Z\n10,20,30\n40,50,60")
            temp_path = f.name

        try:
            self.record.set(self.node._filepath_pin, temp_path)
            self.node.run(self.record)
            result = self.record.get(self.node._output)

            self.assertIsInstance(result, pd.DataFrame)
            self.assertEqual(list(result.columns), ["X", "Y", "Z"])
            self.assertEqual(len(result), 2)
            self.assertEqual(result["X"].tolist(), [10, 40])
        finally:
            os.unlink(temp_path)

    def test_read_csv_with_missing_values(self):
        """Test reading CSV with missing values."""
        csv_data = "A,B,C\n1,2,3\n4,,6\n,8,9"
        buffer = StringIO(csv_data)

        self.record.set(self.node._filepath_pin, buffer)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)
        self.assertTrue(pd.isna(result.iloc[1, 1]))  # Missing B in row 2
        self.assertTrue(pd.isna(result.iloc[2, 0]))  # Missing A in row 3

    def test_read_csv_with_quoted_fields(self):
        """Test reading CSV with quoted fields."""
        csv_data = 'name,description,value\nitem1,"A long, detailed description",100\nitem2,"Another description",200'
        buffer = StringIO(csv_data)

        self.record.set(self.node._filepath_pin, buffer)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertEqual(result["description"].iloc[0], "A long, detailed description")

    def test_read_csv_mixed_data_types(self):
        """Test reading CSV with mixed data types."""
        csv_data = "string_col,int_col,float_col,bool_col\ntest,1,1.5,True\nhello,2,2.7,False"
        buffer = StringIO(csv_data)

        self.record.set(self.node._filepath_pin, buffer)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertEqual(result["string_col"].tolist(), ["test", "hello"])
        self.assertEqual(result["int_col"].tolist(), [1, 2])

    def test_read_csv_empty_file(self):
        """Test reading empty CSV."""
        csv_data = ""
        buffer = StringIO(csv_data)

        self.record.set(self.node._filepath_pin, buffer)

        try:
            self.node.run(self.record)
            result = self.record.get(self.node._output)
            # If it doesn't raise an error, result should be empty DataFrame
            self.assertIsInstance(result, pd.DataFrame)
            self.assertTrue(result.empty)
        except pd.errors.EmptyDataError:
            # This is expected behavior for empty CSV
            pass

    def test_read_csv_header_only(self):
        """Test reading CSV with header only."""
        csv_data = "A,B,C"
        buffer = StringIO(csv_data)

        self.record.set(self.node._filepath_pin, buffer)
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B", "C"])
        self.assertEqual(len(result), 0)  # No data rows

    def test_read_csv_with_tab_separator(self):
        """Test reading TSV (tab-separated) file."""
        tsv_data = "A\tB\tC\n1\t2\t3\n4\t5\t6"
        buffer = StringIO(tsv_data)

        self.record.set(self.node._filepath_pin, buffer)
        self.record.set(self.node._sep_pin, "\t")
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["A", "B", "C"])
        self.assertEqual(len(result), 2)

    def test_read_csv_multi_index_columns(self):
        """Test reading CSV with multiple index columns."""
        csv_data = "id1,id2,value1,value2\n1,a,10,20\n1,b,30,40\n2,a,50,60"
        buffer = StringIO(csv_data)

        self.record.set(self.node._filepath_pin, buffer)
        self.record.set(self.node._index_col_pin, [0, 1])
        self.node.run(self.record)
        result = self.record.get(self.node._output)

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["value1", "value2"])
        # Should have multi-index
        self.assertTrue(isinstance(result.index, pd.MultiIndex))

    def test_node_pins(self):
        """Test node pin configuration."""
        self.assertTrue(hasattr(self.node, "_filepath_pin"))
        self.assertTrue(hasattr(self.node, "_sep_pin"))
        self.assertTrue(hasattr(self.node, "_header_pin"))
        self.assertTrue(hasattr(self.node, "_index_col_pin"))
        self.assertTrue(hasattr(self.node, "_output"))

        self.assertEqual(self.node._filepath_pin.name.value, "filepath_or_buffer")
        self.assertEqual(self.node._sep_pin.name.value, "sep")
        self.assertEqual(self.node._header_pin.name.value, "header")
        self.assertEqual(self.node._index_col_pin.name.value, "index_col")

        self.assertTrue(self.node._filepath_pin.required)
        self.assertFalse(self.node._sep_pin.required)
        self.assertFalse(self.node._header_pin.required)
        self.assertFalse(self.node._index_col_pin.required)


if __name__ == "__main__":
    main()