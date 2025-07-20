# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.units.byte import (
    EB_TO_BYTES,
    GB_TO_BYTES,
    KB_TO_BYTES,
    MB_TO_BYTES,
    PB_TO_BYTES,
    TB_TO_BYTES,
    ZB_TO_BYTES,
)


class ByteTestCase(TestCase):
    def test_default(self):
        self.assertEqual(KB_TO_BYTES, 1024)
        self.assertEqual(MB_TO_BYTES, 1024 * 1024)
        self.assertEqual(GB_TO_BYTES, 1024 * 1024 * 1024)
        self.assertEqual(TB_TO_BYTES, 1024 * 1024 * 1024 * 1024)
        self.assertEqual(PB_TO_BYTES, 1024 * 1024 * 1024 * 1024 * 1024)
        self.assertEqual(EB_TO_BYTES, 1024 * 1024 * 1024 * 1024 * 1024 * 1024)
        self.assertEqual(ZB_TO_BYTES, 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024)


if __name__ == "__main__":
    main()
