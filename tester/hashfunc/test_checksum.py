# -*- coding: utf-8 -*-

from unittest import TestCase, main

from cvp.hashfunc.checksum import HashFunction, checksum


class ChecksumTestCase(TestCase):
    def test_sha1(self):
        self.assertEqual("cbf53a1c", checksum(HashFunction.crc32, b"12345"))
        self.assertEqual(
            "8cb2237d0679ca88db6464eac60da96345513964",
            checksum(HashFunction.sha1, b"12345"),
        )


if __name__ == "__main__":
    main()
