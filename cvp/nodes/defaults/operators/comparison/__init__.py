# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Optional, Sequence, Type

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults.operators.comparison.equal import EqualNode
from cvp.nodes.defaults.operators.comparison.greater import GreaterNode
from cvp.nodes.defaults.operators.comparison.greater_equal import GreaterEqualNode
from cvp.nodes.defaults.operators.comparison.less import LessNode
from cvp.nodes.defaults.operators.comparison.less_equal import LessEqualNode
from cvp.nodes.defaults.operators.comparison.not_equal import NotEqualNode
from cvp.nodes.node import Node


@lru_cache
def get_comparison_types() -> Sequence[Type]:
    return (
        EqualNode,
        GreaterNode,
        GreaterEqualNode,
        LessNode,
        LessEqualNode,
        NotEqualNode,
    )


def get_comparison_nodes(
    dtype_registry: Optional[DtypeRegistry] = None,
) -> Sequence[Node]:
    if dtype_registry is None:
        dtype_registry = global_dtype_registry()
    assert dtype_registry is not None
    return tuple(cls(dtype_registry) for cls in get_comparison_types())
