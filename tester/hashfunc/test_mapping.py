# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.hashfunc.mapping import HashFunction, compute_hash


class MappingTestCase(TestCase):
    def test_sha1(self):
        self.assertEqual("cbf53a1c", compute_hash(HashFunction.crc32, b"12345"))
        self.assertEqual(
            "8cb2237d0679ca88db6464eac60da96345513964",
            compute_hash(HashFunction.sha1, b"12345"),
        )


if __name__ == "__main__":
    main()
