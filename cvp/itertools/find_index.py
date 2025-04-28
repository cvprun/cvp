# -*- coding: utf-8 -*-

from typing import Callable, Iterable, TypeVar

from cvp.variables import NOT_FOUND_INDEX

_T = TypeVar("_T")


def find_index(iterable: Iterable[_T], key: Callable[[_T], bool]) -> int:
    for i, item in enumerate(iterable):
        if key(item):
            return i
    return NOT_FOUND_INDEX
