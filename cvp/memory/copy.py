# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import Enum, auto, unique
from typing import TypeVar

_T = TypeVar("_T")


def copy_flexible(obj: _T, *, use_copy=False, use_deepcopy=False) -> _T:
    if use_copy and use_deepcopy:
        raise ValueError("use_copy and use_deepcopy cannot coexist")

    if use_copy:
        return copy(obj)
    elif use_deepcopy:
        return deepcopy(obj)
    else:
        return obj


@unique
class CopyMethod(Enum):
    assign = auto()
    copy = auto()
    deepcopy = auto()


def copy_with_method(obj: _T, method: CopyMethod) -> _T:
    match method:
        case CopyMethod.assign:
            return obj
        case CopyMethod.copy:
            return copy(obj)
        case CopyMethod.deepcopy:
            return deepcopy(obj)
        case _:
            assert False, "Inaccessible section"
