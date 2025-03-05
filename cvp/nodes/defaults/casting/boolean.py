# -*- coding: utf-8 -*-

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults.casting._base import CastingNodeTemplate


class BooleanNodeTemplate(CastingNodeTemplate):
    def __init__(self, dtype_registry: DtypeRegistry):
        super().__init__(dtype_registry, bool)
