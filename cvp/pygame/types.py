# -*- coding: utf-8 -*-

from os import PathLike
from typing import (
    IO,
    Protocol,
    SupportsIndex,
    Tuple,
    TypeVar,
    Union,
    runtime_checkable,
)

AnyPath = Union[str, bytes, PathLike[str], PathLike[bytes]]
FileArg = Union[AnyPath, IO[bytes], IO[str]]

_T = TypeVar("_T", covariant=True)


@runtime_checkable
class SequenceProtocol(Protocol[_T]):
    def __getitem__(self, __i: SupportsIndex) -> _T: ...
    def __len__(self) -> int: ...


Coordinate = SequenceProtocol[float]
IntCoordinate = SequenceProtocol[int]

RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[int, str, SequenceProtocol[int]]
