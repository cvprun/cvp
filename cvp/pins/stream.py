# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique
from typing import Literal, Union


@unique
class Stream(StrEnum):
    input = auto()
    """
    The standard input stream number is 0.
    """

    output = auto()
    """
    The standard output stream number is 1.
    """


StreamLiteral = Literal["input", "output", 0, 1]
AnyStream = Union[Stream, StreamLiteral]


def create_stream(value: AnyStream) -> Stream:
    if isinstance(value, Stream):
        return value
    elif isinstance(value, str):
        match value.lower():
            case "input":
                return Stream.input
            case "output":
                return Stream.output
            case _:
                raise ValueError(f"Unsupported stream value: {value}")
    elif isinstance(value, int):
        match value:
            case 0:
                return Stream.input
            case 1:
                return Stream.output
            case _:
                raise ValueError(f"Unsupported stream value: {value}")
    else:
        raise TypeError(f"Unsupported stream type: {type(value).__name__}")
