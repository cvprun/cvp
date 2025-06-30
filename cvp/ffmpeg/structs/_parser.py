# -*- coding: utf-8 -*-

from typing import List, Protocol, Self, Sequence, Type, TypeVar


class FormatLineProtocol(Protocol):
    name: str

    def __repr__(self): ...

    @classmethod
    def from_format_line(cls, line: str) -> Self: ...


_T = TypeVar("_T", bound=FormatLineProtocol)


def parse_ffmpeg_format_output(
    text: str,
    header_lines: Sequence[str],
    cls: Type[_T],
) -> List[_T]:
    lines = text.splitlines()
    for i, header_line in enumerate(header_lines):
        if lines[i] != header_line:
            raise ValueError(f"This is not the expected header line #{i}: '{lines[i]}'")

    begin = len(header_lines)
    lines = lines[begin:]

    # [IMPORTANT] Do not use strip
    return [cls.from_format_line(line) for line in lines]
