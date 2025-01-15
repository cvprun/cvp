# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

import numpy

from cvp.dtypes.dtype import Dtype


@lru_cache
def get_extra_types() -> Sequence[Type]:
    return (numpy.ndarray,)


@lru_cache
def get_extra_dtypes() -> Sequence[Dtype]:
    return tuple(Dtype(cls) for cls in get_extra_types())
