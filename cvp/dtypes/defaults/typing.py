# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Any, Sequence

from cvp.dtypes.dtype import Dtype


@lru_cache
def get_typing_any() -> Dtype:
    """
    This is the default type for handling unknown types.
    """
    assert isinstance(Any, type)
    return Dtype(Any, hidden=True)  # type: ignore[arg-type]


@lru_cache
def get_typing_dtypes() -> Sequence[Dtype]:
    return (get_typing_any(),)
