# -*- coding: utf-8 -*-

from functools import lru_cache
from types import MappingProxyType
from typing import Optional

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.node import Node

NodeMapping = MappingProxyType[str, Node]


@lru_cache
def get_default_nodes(dtype_registry: Optional[DtypeRegistry] = None) -> NodeMapping:
    if dtype_registry is None:
        dtype_registry = global_dtype_registry()
    assert dtype_registry is not None
    return NodeMapping({})
