# -*- coding: utf-8 -*-
# https://docs.python.org/3/library/stdtypes.html

from functools import lru_cache
from typing import Any, Sequence, Type

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
def get_typing_any() -> Dtype:
    """
    This is the default type for handling unknown types.
    """
    assert isinstance(Any, type)
    return Dtype(Any)  # type: ignore[arg-type]


@lru_cache
def get_builtin_dtypes() -> Sequence[Dtype]:
    return tuple([Dtype(cls) for cls in get_builtin_types()] + [get_typing_any()])
