# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

from cvp.nodes.defaults.essential.empty import Empty
from cvp.nodes.defaults.essential.entrypoint import Entrypoint
from cvp.nodes.defaults.essential.getter import Getter
from cvp.nodes.defaults.essential.logging import Logging
from cvp.nodes.defaults.essential.setter import Setter
from cvp.nodes.node import Node


@lru_cache
def get_essential_types() -> Sequence[Type]:
    return (
        Empty,
        Entrypoint,
        Logging,
        Getter,
        Setter,
    )


@lru_cache
def get_essential_nodes() -> Sequence[Node]:
    return tuple(cls() for cls in get_essential_types())
