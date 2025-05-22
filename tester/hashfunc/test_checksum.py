# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.hashfunc.checksum import Checksum
from cvp.hashfunc.mapping import HashFunction


class ChecksumTestCase(TestCase):
    def test_crc32(self):
        cs = Checksum.parse("crc32:cbf53a1c")
        self.assertEqual(cs.hash_method, HashFunction.crc32)
        self.assertEqual(cs.hash_value, "cbf53a1c")
        self.assertTrue(cs.verify(b"12345"))

    def test_sha1(self):
        cs = Checksum.parse("sha1:8cb2237d0679ca88db6464eac60da96345513964")
        self.assertEqual(cs.hash_method, HashFunction.sha1)
        self.assertEqual(cs.hash_value, "8cb2237d0679ca88db6464eac60da96345513964")
        self.assertTrue(cs.verify(b"12345"))


if __name__ == "__main__":
    main()
