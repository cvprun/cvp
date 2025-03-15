# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

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


def get_arithmetic_nodes() -> Sequence[Node]:
    return tuple(cls() for cls in get_arithmetic_types())
