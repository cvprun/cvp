# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

from cvp.nodes.defaults.operators.arithmetic.add import AddOperator
from cvp.nodes.defaults.operators.arithmetic.divide import DivideOperator
from cvp.nodes.defaults.operators.arithmetic.multiply import MultiplyOperator
from cvp.nodes.defaults.operators.arithmetic.subtract import SubtractOperator
from cvp.nodes.node import Node


@lru_cache
def get_arithmetic_types() -> Sequence[Type]:
    return (
        AddOperator,
        DivideOperator,
        MultiplyOperator,
        SubtractOperator,
    )


def get_arithmetic_nodes() -> Sequence[Node]:
    return tuple(cls() for cls in get_arithmetic_types())
