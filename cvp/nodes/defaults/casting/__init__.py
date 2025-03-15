# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

from cvp.nodes.defaults.casting.boolean import BooleanNode
from cvp.nodes.defaults.casting.floating import FloatingNode
from cvp.nodes.defaults.casting.integer import IntegerNode
from cvp.nodes.defaults.casting.string import StringNode
from cvp.nodes.node import Node


@lru_cache
def get_casting_types() -> Sequence[Type]:
    return (
        BooleanNode,
        FloatingNode,
        IntegerNode,
        StringNode,
    )


@lru_cache
def get_casting_nodes() -> Sequence[Node]:
    return tuple(cls() for cls in get_casting_types())
