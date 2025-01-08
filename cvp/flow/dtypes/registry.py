# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Dict

from cvp.flow.datas.templates.dtype import Dtype
from cvp.flow.path import FlowPath
from cvp.patterns.singleton import singleton


class FlowDtypeRegistry(Dict[FlowPath, Dtype]):
    def register_dtype(self):
        pass

    def register_class(self):
        pass


@singleton
class GlobalFlowDtypeRegistry(FlowDtypeRegistry):
    pass


@lru_cache
def global_dtype_registry() -> GlobalFlowDtypeRegistry:
    return GlobalFlowDtypeRegistry()


def register_dtype():
    pass
