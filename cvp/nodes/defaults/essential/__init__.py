# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Optional, Sequence, Type

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults.essential.entrypoint import EntrypointNodeTemplate
from cvp.nodes.defaults.essential.getter import GetterNodeTemplate
from cvp.nodes.defaults.essential.logging import LoggingNodeTemplate
from cvp.nodes.defaults.essential.setter import SetterNodeTemplate
from cvp.nodes.template import NodeTemplate


@lru_cache
def get_essential_types() -> Sequence[Type]:
    return (
        EntrypointNodeTemplate,
        LoggingNodeTemplate,
        GetterNodeTemplate,
        SetterNodeTemplate,
    )


@lru_cache
def get_essential_nodes(
    dtype_registry: Optional[DtypeRegistry] = None,
) -> Sequence[NodeTemplate]:
    if dtype_registry is None:
        dtype_registry = global_dtype_registry()
    assert dtype_registry is not None
    return tuple(cls(dtype_registry) for cls in get_essential_types())
