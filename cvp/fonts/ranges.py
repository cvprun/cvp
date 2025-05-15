# -*- coding: utf-8 -*-

from os import PathLike
from typing import List, NamedTuple, Sequence, Union

from cvp.variables import COMMENT_PREFIX, HEXADECIMAL, UNICODE_SINGLE_BLOCK_SIZE


class BlockRange(NamedTuple):
    begin: int
    end: int

    def as_label(self) -> str:
        return f"{self.begin:06X}-{self.end:06X}"


class CodepointRange(NamedTuple):
    begin: int
    end: int

    def as_label(self) -> str:
        return f"{self.begin:06X}-{self.end:06X}"

    def size(self) -> int:
        return abs(self.end - self.begin) + 1

    def has_codepoint(self, codepoint: int) -> bool:
        return self.begin <= codepoint <= self.end

    def as_blocks(self, step=UNICODE_SINGLE_BLOCK_SIZE) -> List[BlockRange]:
        block_begin = (self.begin // step) * step
        block_end = block_begin + step - 1

        assert block_begin <= self.begin
        result = [BlockRange(block_begin, block_end)]

        while block_end < self.end:
            block_begin += step
            block_end += step
            result.append(BlockRange(block_begin, block_end))

        return result


def read_ranges(path: Union[str, PathLike[str]]) -> List[CodepointRange]:
    result = list()
    with open(path, "rt") as file:
        for line in file:
            if line and line.startswith(COMMENT_PREFIX):
                continue
            hex_values = line.strip().split()
            assert len(hex_values) == 2
            begin = int(hex_values[0].strip(), HEXADECIMAL)
            end = int(hex_values[1].strip(), HEXADECIMAL)
            result.append(CodepointRange(begin, end))
    return result


def flatten_ranges(ranges: Sequence[CodepointRange]) -> List[int]:
    result = list()
    for begin, end in ranges:
        result.append(begin)
        result.append(end)
    return result
