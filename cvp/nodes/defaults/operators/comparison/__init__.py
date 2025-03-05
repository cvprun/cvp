# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Optional, Sequence, Type

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults.operators.comparison.equal import EqualNodeTemplate
from cvp.nodes.defaults.operators.comparison.greater import GreaterNodeTemplate
from cvp.nodes.defaults.operators.comparison.greater_equal import (
    GreaterEqualNodeTemplate,
)
from cvp.nodes.defaults.operators.comparison.less import LessNodeTemplate
from cvp.nodes.defaults.operators.comparison.less_equal import LessEqualNodeTemplate
from cvp.nodes.defaults.operators.comparison.not_equal import NotEqualNodeTemplate
from cvp.nodes.template import NodeTemplate


@lru_cache
def get_comparison_types() -> Sequence[Type]:
    return (
        EqualNodeTemplate,
        GreaterNodeTemplate,
        GreaterEqualNodeTemplate,
        LessNodeTemplate,
        LessEqualNodeTemplate,
        NotEqualNodeTemplate,
    )


def get_comparison_nodes(
    dtype_registry: Optional[DtypeRegistry] = None,
) -> Sequence[NodeTemplate]:
    if dtype_registry is None:
        dtype_registry = global_dtype_registry()
    assert dtype_registry is not None
    return tuple(cls(dtype_registry) for cls in get_comparison_types())
