# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Dict, Sequence, Type

import numpy

from cvp.flow.templates.dtype import Dtype


@lru_cache
def get_extra_types() -> Sequence[Type]:
    return (numpy.ndarray,)


@lru_cache
def get_extra_dtypes() -> Dict[Type, Dtype]:
    return {cls: Dtype(cls) for cls in get_extra_types()}
