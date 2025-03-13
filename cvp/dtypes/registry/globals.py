# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Optional

from cvp.dtypes.dtype import DtypeName
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.fonts.types import IconCode
from cvp.modules.class_path import TypePath
from cvp.patterns.singleton import singleton
from cvp.types.colors import RGBA


@singleton
class GlobalDtypeRegistry(DtypeRegistry):
    pass


@lru_cache
def global_dtype_registry() -> GlobalDtypeRegistry:
    return GlobalDtypeRegistry()


def register_dtype(
    name: Optional[DtypeName] = None,
    docs: Optional[str] = None,
    icon: Optional[IconCode] = None,
    color: Optional[RGBA] = None,
):
    return global_dtype_registry().register(name, docs, icon, color)
