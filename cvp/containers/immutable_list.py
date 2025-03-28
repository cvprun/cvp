# -*- coding: utf-8 -*-

from typing import Generic, Iterable, List, SupportsIndex, TypeVar

_T = TypeVar("_T")


class ImmutableList(List[_T], Generic[_T]):
    def __init__(self, __iterable: Iterable[_T]):
        super().__init__(__iterable)

    def __setitem__(self, __key, __value) -> None:
        raise NotImplementedError

    def __delitem__(self, __key) -> None:
        raise NotImplementedError

    def __iadd__(self, __value):  # type: ignore[misc]
        raise NotImplementedError

    def __imul__(self, __value):  # type: ignore[misc]
        raise NotImplementedError

    def append(self, __object: _T) -> None:
        raise NotImplementedError

    def extend(self, __iterable: Iterable[_T]) -> None:
        raise NotImplementedError

    def insert(self, __index: SupportsIndex, __object: _T) -> None:
        raise NotImplementedError

    def pop(self, __index: SupportsIndex = -1) -> _T:
        raise NotImplementedError

    def remove(self, __value: _T) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    def sort(self, *, key=None, reverse=False) -> None:
        raise NotImplementedError

    def reverse(self) -> None:
        raise NotImplementedError
