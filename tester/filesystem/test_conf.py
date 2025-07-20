# -*- coding: utf-8 -*-

from tempfile import NamedTemporaryFile
from unittest import TestCase, main

from cvp.filesystem.conf import get_block_size


class ConfTestCase(TestCase):
    def test_get_block_size(self):
        with NamedTemporaryFile() as f:
            block_size = get_block_size(f.name)
            self.assertLess(0, block_size)
            self.assertEqual(0, block_size % 1024)


if __name__ == "__main__":
    main()
