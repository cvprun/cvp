# -*- coding: utf-8 -*-
# https://docs.python.org/3/library/stdtypes.html

from functools import lru_cache
from typing import Any, Dict, Sequence, Type

from cvp.flow.templates.dtype import Dtype


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
    assert isinstance(Any, type)
    return Dtype(Any)  # type: ignore[arg-type]


@lru_cache
def get_builtin_dtypes() -> Dict[Type, Dtype]:
    result = {cls: Dtype(cls) for cls in get_builtin_types()}
    assert isinstance(Any, type)
    assert Any not in result
    result[Any] = get_typing_any()
    return result
