# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Optional, Sequence, Type

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults.essential.entrypoint import EntrypointNode
from cvp.nodes.defaults.essential.getter import VariableGetterNode
from cvp.nodes.defaults.essential.logging import LoggingNode
from cvp.nodes.defaults.essential.setter import VariableSetterNode
from cvp.nodes.node import Node


@lru_cache
def get_essential_types() -> Sequence[Type]:
    return (
        EntrypointNode,
        LoggingNode,
        VariableGetterNode,
        VariableSetterNode,
    )


@lru_cache
def get_essential_nodes(
    dtype_registry: Optional[DtypeRegistry] = None,
) -> Sequence[Node]:
    if dtype_registry is None:
        dtype_registry = global_dtype_registry()
    assert dtype_registry is not None
    return tuple(cls(dtype_registry) for cls in get_essential_types())
