# -*- coding: utf-8 -*-

from functools import lru_cache
from types import MappingProxyType
from typing import Final, List, Sequence, Type

from cvp.dtypes.defaults.builtins import get_builtin_dtypes
from cvp.dtypes.defaults.extras import get_extra_dtypes
from cvp.dtypes.defaults.standards import get_standard_dtypes
from cvp.dtypes.defaults.typing import get_typing_dtypes
from cvp.dtypes.dtype import Dtype
from cvp.modules.class_path import TypePath

TypeToDtypeMapping = MappingProxyType[Type, Dtype]
PathToDtypeMapping = MappingProxyType[TypePath, Dtype]


@lru_cache
def get_default_dtypes() -> Sequence[Dtype]:
    result: List[Dtype] = list()
    result.extend(get_builtin_dtypes())
    result.extend(get_standard_dtypes())
    result.extend(get_extra_dtypes())
    result.extend(get_typing_dtypes())
    return tuple(result)


@lru_cache
def get_default_type2dtypes() -> TypeToDtypeMapping:
    return TypeToDtypeMapping({dt.base.type: dt for dt in get_default_dtypes()})


@lru_cache
def get_default_path2dtypes() -> PathToDtypeMapping:
    return PathToDtypeMapping({dt.path: dt for dt in get_default_dtypes()})


DEFAULT_TYPE_TO_DTYPES: Final[TypeToDtypeMapping] = get_default_type2dtypes()
DEFAULT_PATH_TO_DTYPES: Final[PathToDtypeMapping] = get_default_path2dtypes()
