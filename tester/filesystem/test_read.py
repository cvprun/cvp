# -*- coding: utf-8 -*-

from tempfile import NamedTemporaryFile
from unittest import TestCase, main

from cvp.concurrency.threading.progress_value import ProgressValue
from cvp.filesystem.read import read_progressive
from cvp.units.byte import BYTES_10MB


class ReadTestCase(TestCase):
    def test_read_progressive_reads_correct_content(self):
        test_content = "Hello, world!\nThis is a test file.\n한글도 가능 합니다."
        encoded_content = test_content.encode()

        progress = ProgressValue(limit=len(encoded_content))
        self.assertEqual(len(encoded_content), progress.limit)
        self.assertEqual(0, progress.value)

        with NamedTemporaryFile() as f:
            self.assertEqual(len(encoded_content), f.write(encoded_content))
            f.flush()
            f.seek(0)

            result = read_progressive(f.name, progress=progress)
            self.assertEqual(result, test_content)
            self.assertEqual(len(encoded_content), progress.limit)
            self.assertEqual(len(encoded_content), progress.value)

    def test_read_progressive_empty_file(self):
        with NamedTemporaryFile() as f:
            result = read_progressive(f.name)
            self.assertEqual("", result)

    def test_read_progressive_large_file(self):
        large_text = "A" * BYTES_10MB
        encoded_content = large_text.encode()

        progress = ProgressValue(limit=len(encoded_content))
        self.assertEqual(len(encoded_content), progress.limit)
        self.assertEqual(0, progress.value)

        with NamedTemporaryFile() as f:
            self.assertEqual(len(encoded_content), f.write(encoded_content))
            f.flush()
            f.seek(0)

            result = read_progressive(f.name, progress=progress)
            self.assertEqual(result, large_text)
            self.assertEqual(len(encoded_content), progress.limit)
            self.assertEqual(len(encoded_content), progress.value)


if __name__ == "__main__":
    main()
