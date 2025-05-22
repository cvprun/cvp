# -*- coding: utf-8 -*-

from typing import NamedTuple

from cvp.hashfunc.mapping import HashFunction, compute_hash
from cvp.variables import CHECKSUM_DELIMITER


class Checksum(NamedTuple):
    hash_method: HashFunction
    hash_value: str

    def __str__(self) -> str:
        return f"{str(self.hash_method)}{CHECKSUM_DELIMITER}{self.hash_value}"

    @classmethod
    def parse(cls, method_value: str, delimiter=CHECKSUM_DELIMITER):
        method, value = method_value.split(delimiter, 1)
        assert isinstance(method, str)
        assert isinstance(value, str)
        return cls(HashFunction(method.strip().lower()), value.strip())

    def verify(self, data: bytes) -> bool:
        return compute_hash(self.hash_method, data) == self.hash_value
