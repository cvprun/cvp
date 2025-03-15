# -*- coding: utf-8 -*-

from functools import lru_cache

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.patterns.singleton import singleton


@singleton
class GlobalDtypeRegistry(DtypeRegistry):
    pass


@lru_cache
def global_dtype_registry() -> GlobalDtypeRegistry:
    return GlobalDtypeRegistry()


def register_dtype():
    return global_dtype_registry().register()
