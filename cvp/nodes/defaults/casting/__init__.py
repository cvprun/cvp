# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

from cvp.nodes.defaults.casting.boolean import BooleanCasting
from cvp.nodes.defaults.casting.floating import FloatingCasting
from cvp.nodes.defaults.casting.integer import IntegerCasting
from cvp.nodes.defaults.casting.string import StringCasting
from cvp.nodes.node import Node


@lru_cache
def get_casting_types() -> Sequence[Type]:
    return (
        BooleanCasting,
        FloatingCasting,
        IntegerCasting,
        StringCasting,
    )


@lru_cache
def get_casting_nodes() -> Sequence[Node]:
    return tuple(cls() for cls in get_casting_types())
