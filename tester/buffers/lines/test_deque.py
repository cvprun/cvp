# -*- coding: utf-8 -*-

import os
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest import TestCase, main

from cvp.buffers.lines.deque import LinesDeque


class DequeTestCase(TestCase):
    def test_default(self):
        with TemporaryDirectory() as tmpdir:
            self.assertTrue(os.path.isdir(tmpdir))

            with NamedTemporaryFile("wt", dir=tmpdir) as f:
                with LinesDeque(f.name, maxlen=2) as deque:
                    self.assertEqual("", deque.getvalue())
                    self.assertEqual(5, f.write("12345"))
                    self.assertEqual(0, os.path.getsize(f.name))
                    f.flush()

                    self.assertEqual(5, os.path.getsize(f.name))

                    deque.update()
                    self.assertEqual(1, len(deque.lines))
                    self.assertEqual("12345", deque.lines[0])
                    self.assertEqual("12345", deque.getvalue())

                    self.assertEqual(5, f.write("67890"))
                    f.flush()
                    self.assertEqual(10, os.path.getsize(f.name))

                    deque.update()
                    self.assertEqual(1, len(deque.lines))
                    self.assertEqual("1234567890", deque.lines[0])
                    self.assertEqual("1234567890", deque.getvalue())

                    self.assertEqual(6, f.write("\nabcde"))
                    f.flush()
                    self.assertEqual(16, os.path.getsize(f.name))

                    deque.update()
                    self.assertEqual(2, len(deque.lines))
                    self.assertEqual("1234567890", deque.lines[0])
                    self.assertEqual("abcde", deque.lines[1])
                    self.assertEqual("1234567890\nabcde", deque.getvalue())

                    self.assertEqual(10, f.write("-zxcv\nqwer"))
                    f.flush()
                    self.assertEqual(26, os.path.getsize(f.name))

                    deque.update()
                    self.assertEqual(2, len(deque.lines))
                    self.assertEqual("abcde-zxcv", deque.lines[0])
                    self.assertEqual("qwer", deque.lines[1])
                    self.assertEqual("abcde-zxcv\nqwer", deque.getvalue())

                    self.assertEqual(1, f.write("\n"))
                    f.flush()
                    self.assertEqual(27, os.path.getsize(f.name))

                    deque.update()
                    self.assertEqual(2, len(deque.lines))
                    self.assertEqual("qwer", deque.lines[0])
                    self.assertEqual("", deque.lines[1])
                    self.assertEqual("qwer\n", deque.getvalue())


if __name__ == "__main__":
    main()
