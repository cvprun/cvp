# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Optional

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.patterns.singleton import singleton
from cvp.types.colors import RGBA


@singleton
class GlobalDtypeRegistry(DtypeRegistry):
    pass


@lru_cache
def global_registry() -> GlobalDtypeRegistry:
    return GlobalDtypeRegistry()


def register_dtype(
    name: Optional[str] = None,
    path: Optional[str] = None,
    docs: Optional[str] = None,
    icon: Optional[str] = None,
    color: Optional[RGBA] = None,
):
    return global_registry().register(name, path, docs, icon, color)
