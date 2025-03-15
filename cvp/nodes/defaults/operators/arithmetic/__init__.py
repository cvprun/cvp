# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

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


def get_arithmetic_nodes() -> Sequence[NodeTemplate]:
    return tuple(cls() for cls in get_arithmetic_types())
