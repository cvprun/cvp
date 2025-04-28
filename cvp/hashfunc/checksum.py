# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/List_of_hash_functions

import hashlib
import zlib
from enum import StrEnum, auto, unique
from typing import Callable, Dict, Final


@unique
class HashFunction(StrEnum):
    blake2b = auto()
    blake2s = auto()
    crc32 = auto()
    md5 = auto()
    sha1 = auto()
    sha224 = auto()
    sha256 = auto()
    sha384 = auto()
    sha3_224 = auto()
    sha3_256 = auto()
    sha3_384 = auto()
    sha3_512 = auto()
    sha512 = auto()
    shake_128 = auto()
    shake_256 = auto()


class _Crc32:
    def __init__(self, data: bytes):
        self._checksum = zlib.crc32(data) & 0xFFFFFFFF

    @property
    def checksum(self) -> int:
        return self._checksum

    def hexdigest(self) -> str:
        return "{0:x}".format(self._checksum)


_HASH_FUNCS: Final[Dict[HashFunction, Callable]] = {
    HashFunction.blake2b: hashlib.blake2b,
    HashFunction.blake2s: hashlib.blake2s,
    HashFunction.crc32: _Crc32,
    HashFunction.md5: hashlib.md5,
    HashFunction.sha1: hashlib.sha1,
    HashFunction.sha224: hashlib.sha224,
    HashFunction.sha256: hashlib.sha256,
    HashFunction.sha384: hashlib.sha384,
    HashFunction.sha3_224: hashlib.sha3_224,
    HashFunction.sha3_256: hashlib.sha3_256,
    HashFunction.sha3_384: hashlib.sha3_384,
    HashFunction.sha3_512: hashlib.sha3_512,
    HashFunction.sha512: hashlib.sha512,
    HashFunction.shake_128: hashlib.shake_128,
    HashFunction.shake_256: hashlib.shake_256,
}


def checksum(method: HashFunction, data: bytes) -> str:
    return _HASH_FUNCS[method](data).hexdigest()
