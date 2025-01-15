# -*- coding: utf-8 -*-

from functools import lru_cache
from types import MappingProxyType
from typing import Final, Optional, Type

from cvp.flow.catalog.dtype.builtins import get_builtin_dtypes
from cvp.flow.catalog.dtype.extra import get_extra_dtypes
from cvp.flow.catalog.dtype.standard import get_standard_dtypes
from cvp.flow.templates.dtype import Dtype

DtypeMapping = MappingProxyType[Type, Dtype]


@lru_cache
def get_default_dtypes() -> DtypeMapping:
    mapping = dict()
    mapping.update(get_builtin_dtypes())
    mapping.update(get_standard_dtypes())
    mapping.update(get_extra_dtypes())
    return DtypeMapping(mapping)


DEFAULT_DTYPES: Final[DtypeMapping] = get_default_dtypes()


def get_default_dtype(base: type) -> Optional[Dtype]:
    return DEFAULT_DTYPES.get(base)
