# -*- coding: utf-8 -*-

from typing import List, Optional, Sequence

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults.operators.arithmetic import get_arithmetic_nodes
from cvp.nodes.defaults.operators.comparison import get_comparison_nodes
from cvp.nodes.node import Node


def get_operators_nodes(
    dtype_registry: Optional[DtypeRegistry] = None,
) -> Sequence[Node]:
    if dtype_registry is None:
        dtype_registry = global_dtype_registry()
    assert dtype_registry is not None
    result: List[Node] = list()
    result.extend(get_arithmetic_nodes(dtype_registry))
    result.extend(get_comparison_nodes(dtype_registry))
    return tuple(result)
