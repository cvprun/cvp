# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

from cvp.nodes.defaults.essential.entrypoint import EntrypointNode
from cvp.nodes.defaults.essential.getter import GetterNode
from cvp.nodes.defaults.essential.logging import LoggingNode
from cvp.nodes.defaults.essential.setter import SetterNode
from cvp.nodes.node import Node


@lru_cache
def get_essential_types() -> Sequence[Type]:
    return (
        EntrypointNode,
        LoggingNode,
        GetterNode,
        SetterNode,
    )


@lru_cache
def get_essential_nodes() -> Sequence[Node]:
    return tuple(cls() for cls in get_essential_types())
