# -*- coding: utf-8 -*-

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults.casting._base import CastingNodeTemplate


class FloatingNodeTemplate(CastingNodeTemplate):
    def __init__(self, dtype_registry: DtypeRegistry):
        super().__init__(dtype_registry, float)
