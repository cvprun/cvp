# -*- coding: utf-8 -*-
# https://docs.python.org/3/library/stdtypes.html

from functools import lru_cache
from typing import Sequence, Type

from cvp.dtypes.dtype import Dtype


@lru_cache
def get_builtin_types() -> Sequence[Type]:
    return (
        type(None),
        int,
        float,
        complex,
        bool,
        list,
        tuple,
        range,
        bytes,
        bytearray,
        set,
        frozenset,
        dict,
        str,
        memoryview,
        object,
    )


@lru_cache
def get_builtin_dtypes() -> Sequence[Dtype]:
    return tuple(Dtype(cls) for cls in get_builtin_types())
