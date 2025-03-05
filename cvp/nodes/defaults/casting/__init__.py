# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Optional, Sequence, Type

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults.casting.boolean import BooleanNodeTemplate
from cvp.nodes.defaults.casting.floating import FloatingNodeTemplate
from cvp.nodes.defaults.casting.integer import IntegerNodeTemplate
from cvp.nodes.defaults.casting.string import StringNodeTemplate
from cvp.nodes.template import NodeTemplate


@lru_cache
def get_casting_types() -> Sequence[Type]:
    return (
        BooleanNodeTemplate,
        FloatingNodeTemplate,
        IntegerNodeTemplate,
        StringNodeTemplate,
    )


@lru_cache
def get_casting_nodes(
    dtype_registry: Optional[DtypeRegistry] = None,
) -> Sequence[NodeTemplate]:
    if dtype_registry is None:
        dtype_registry = global_dtype_registry()
    assert dtype_registry is not None
    return tuple(cls(dtype_registry) for cls in get_casting_types())
