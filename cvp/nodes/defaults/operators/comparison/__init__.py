# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

from cvp.nodes.defaults.operators.comparison.equal import EqualOperator
from cvp.nodes.defaults.operators.comparison.greater import GreaterOperator
from cvp.nodes.defaults.operators.comparison.greater_equal import GreaterEqualOperator
from cvp.nodes.defaults.operators.comparison.less import LessOperator
from cvp.nodes.defaults.operators.comparison.less_equal import LessEqualOperator
from cvp.nodes.defaults.operators.comparison.not_equal import NotEqualOperator
from cvp.nodes.node import Node


@lru_cache
def get_comparison_types() -> Sequence[Type]:
    return (
        EqualOperator,
        GreaterOperator,
        GreaterEqualOperator,
        LessOperator,
        LessEqualOperator,
        NotEqualOperator,
    )


def get_comparison_nodes() -> Sequence[Node]:
    return tuple(cls() for cls in get_comparison_types())
