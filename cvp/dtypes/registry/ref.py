# -*- coding: utf-8 -*-

from typing import Optional
from weakref import ReferenceType, ref

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry


class DtypeRegistryRef:
    _ref: ReferenceType[DtypeRegistry]

    def __init__(self, dtype_registry: DtypeRegistry):
        self._ref = ref(dtype_registry)

    @staticmethod
    def get_global() -> DtypeRegistry:
        return global_dtype_registry()

    def get_ref(self) -> Optional[DtypeRegistry]:
        return self._ref()

    def get_force(self) -> DtypeRegistry:
        if registry := self.get_ref():
            return registry
        else:
            return global_dtype_registry()

    def __call__(self) -> DtypeRegistry:
        return self.get_force()
