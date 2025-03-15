# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

from cvp.nodes.defaults.casting.boolean import BooleanNodeTemplate
from cvp.nodes.defaults.casting.floating import FloatingNodeTemplate
from cvp.nodes.defaults.casting.integer import IntegerNodeTemplate
from cvp.nodes.defaults.casting.string import StringNodeTemplate
from cvp.nodes.template import NodeTemplate


@lru_cache
def get_casting_types() -> Sequence[Type]:
    return (
        BooleanNodeTemplate,
        FloatingNodeTemplate,
        IntegerNodeTemplate,
        StringNodeTemplate,
    )


@lru_cache
def get_casting_nodes() -> Sequence[NodeTemplate]:
    return tuple(cls() for cls in get_casting_types())
