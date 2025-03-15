# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

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


def get_comparison_nodes() -> Sequence[NodeTemplate]:
    return tuple(cls() for cls in get_comparison_types())
