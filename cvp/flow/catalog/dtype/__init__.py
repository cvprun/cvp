# -*- coding: utf-8 -*-

from functools import lru_cache
from types import MappingProxyType
from typing import Final, List, Sequence, Type

from cvp.flow.catalog.dtype.builtins import get_builtin_dtypes
from cvp.flow.catalog.dtype.extra import get_extra_dtypes
from cvp.flow.catalog.dtype.standard import get_standard_dtypes
from cvp.flow.templates.dtype import Dtype

TypeToDtypeMapping = MappingProxyType[Type, Dtype]
PathToDtypeMapping = MappingProxyType[str, Dtype]


@lru_cache
def get_default_dtypes() -> Sequence[Dtype]:
    result: List[Dtype] = list()
    result.extend(get_builtin_dtypes())
    result.extend(get_standard_dtypes())
    result.extend(get_extra_dtypes())
    return tuple(result)


@lru_cache
def get_default_type2dtypes() -> TypeToDtypeMapping:
    return TypeToDtypeMapping({dtype.base: dtype for dtype in get_default_dtypes()})


@lru_cache
def get_default_path2dtypes() -> PathToDtypeMapping:
    return PathToDtypeMapping({dtype.path: dtype for dtype in get_default_dtypes()})


DEFAULT_TYPE_TO_DTYPES: Final[TypeToDtypeMapping] = get_default_type2dtypes()
DEFAULT_PATH_TO_DTYPES: Final[PathToDtypeMapping] = get_default_path2dtypes()
