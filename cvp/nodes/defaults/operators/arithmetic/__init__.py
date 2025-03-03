# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Optional, Sequence, Type

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults.operators.arithmetic.add import AddNode
from cvp.nodes.defaults.operators.arithmetic.divide import DivideNode
from cvp.nodes.defaults.operators.arithmetic.multiply import MultiplyNode
from cvp.nodes.defaults.operators.arithmetic.subtract import SubtractNode
from cvp.nodes.node import Node


@lru_cache
def get_arithmetic_types() -> Sequence[Type]:
    return (
        AddNode,
        DivideNode,
        MultiplyNode,
        SubtractNode,
    )


def get_arithmetic_nodes(
    dtype_registry: Optional[DtypeRegistry] = None,
) -> Sequence[Node]:
    if dtype_registry is None:
        dtype_registry = global_dtype_registry()
    assert dtype_registry is not None
    return tuple(cls(dtype_registry) for cls in get_arithmetic_types())
