# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Optional, Sequence, Type

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults.operators.arithmetic.add import AddNodeTemplate
from cvp.nodes.defaults.operators.arithmetic.divide import DivideNodeTemplate
from cvp.nodes.defaults.operators.arithmetic.multiply import MultiplyNodeTemplate
from cvp.nodes.defaults.operators.arithmetic.subtract import SubtractNodeTemplate
from cvp.nodes.template import NodeTemplate


@lru_cache
def get_arithmetic_types() -> Sequence[Type]:
    return (
        AddNodeTemplate,
        DivideNodeTemplate,
        MultiplyNodeTemplate,
        SubtractNodeTemplate,
    )


def get_arithmetic_nodes(
    dtype_registry: Optional[DtypeRegistry] = None,
) -> Sequence[NodeTemplate]:
    if dtype_registry is None:
        dtype_registry = global_dtype_registry()
    assert dtype_registry is not None
    return tuple(cls(dtype_registry) for cls in get_arithmetic_types())
