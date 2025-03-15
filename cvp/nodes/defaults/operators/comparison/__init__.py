# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

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


def get_comparison_nodes() -> Sequence[Node]:
    return tuple(cls() for cls in get_comparison_types())
