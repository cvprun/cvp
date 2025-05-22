# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.hashfunc.mapping import HashFunction, compute_hash


class MappingTestCase(TestCase):
    def test_crc32(self):
        expect = "cbf53a1c"
        actual = compute_hash(HashFunction.crc32, b"12345")
        self.assertEqual(expect, actual)

    def test_sha1(self):
        expect = "8cb2237d0679ca88db6464eac60da96345513964"
        actual = compute_hash(HashFunction.sha1, b"12345")
        self.assertEqual(expect, actual)


if __name__ == "__main__":
    main()
