# -*- coding: utf-8 -*-

from typing import Optional
from weakref import ReferenceType, ref

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry


class DtypeRegistryRef:
    _ref: ReferenceType[DtypeRegistry]

    def __init__(self, dtype_registry: Optional[DtypeRegistry] = None):
        if dtype_registry is None:
            dtype_registry = global_dtype_registry()
        assert dtype_registry is not None
        self._ref = ref(dtype_registry)

    def get(self) -> Optional[DtypeRegistry]:
        return self._ref()

    @staticmethod
    def get_global() -> DtypeRegistry:
        return global_dtype_registry()

    def get_force(self) -> DtypeRegistry:
        if registry := self.get():
            return registry
        else:
            return global_dtype_registry()

    def __call__(self) -> DtypeRegistry:
        return self.get_force()
