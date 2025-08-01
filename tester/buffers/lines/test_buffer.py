# -*- coding: utf-8 -*-

import os
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest import TestCase, main

from cvp.buffers.lines.buffer import LinesBuffer


class BufferTestCase(TestCase):
    def test_lines_buffer(self):
        with TemporaryDirectory() as tmpdir:
            self.assertTrue(os.path.isdir(tmpdir))

            with NamedTemporaryFile("wt", dir=tmpdir) as f:
                with LinesBuffer(f.name, maxsize=10) as buffer:
                    self.assertEqual("", buffer.getvalue())
                    self.assertEqual(5, f.write("12345"))
                    self.assertEqual(0, os.path.getsize(f.name))
                    f.flush()
                    self.assertEqual(5, os.path.getsize(f.name))

                    buffer.update()
                    self.assertEqual("12345", buffer.getvalue())

                    self.assertEqual(5, f.write("67890"))
                    f.flush()
                    self.assertEqual(10, os.path.getsize(f.name))

                    buffer.update()
                    self.assertEqual("1234567890", buffer.getvalue())

                    self.assertEqual(6, f.write("\nabcde"))
                    f.flush()
                    self.assertEqual(16, os.path.getsize(f.name))

                    buffer.update()
                    self.assertEqual("7890\nabcde", buffer.getvalue())

                    self.assertEqual(10, f.write("-zxcv\nqwer"))
                    f.flush()
                    self.assertEqual(26, os.path.getsize(f.name))

                    buffer.update()
                    self.assertEqual("-zxcv\nqwer", buffer.getvalue())

                    self.assertEqual(1, f.write("\n"))
                    f.flush()
                    self.assertEqual(27, os.path.getsize(f.name))

                    buffer.update()
                    self.assertEqual("zxcv\nqwer\n", buffer.getvalue())

    def test_lines_buffer_newline(self):
        with TemporaryDirectory() as tmpdir:
            self.assertTrue(os.path.isdir(tmpdir))

            with NamedTemporaryFile("wt", dir=tmpdir) as f:
                with LinesBuffer(f.name, maxsize=15, newline_size=3) as buffer:
                    self.assertEqual("", buffer.getvalue())
                    self.assertEqual(5, f.write("12345"))
                    self.assertEqual(0, os.path.getsize(f.name))
                    f.flush()
                    self.assertEqual(5, os.path.getsize(f.name))

                    buffer.update()
                    self.assertEqual("123\\\n45", buffer.getvalue())

                    self.assertEqual(6, f.write("\n67890"))
                    f.flush()
                    self.assertEqual(11, os.path.getsize(f.name))

                    buffer.update()
                    self.assertEqual("123\\\n45\n678\\\n90", buffer.getvalue())

                    self.assertEqual(1, f.write("\n"))
                    f.flush()
                    self.assertEqual(12, os.path.getsize(f.name))

                    buffer.update()
                    self.assertEqual("23\\\n45\n678\\\n90\n", buffer.getvalue())

                    self.assertEqual(8, f.write("abcdefgh"))
                    f.flush()
                    self.assertEqual(20, os.path.getsize(f.name))

                    buffer.update()
                    self.assertEqual("90\nabc\\\ndef\\\ngh", buffer.getvalue())


if __name__ == "__main__":
    main()
