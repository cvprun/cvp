# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Sequence, Type

from cvp.nodes.defaults.essential.entrypoint import EntrypointNodeTemplate
from cvp.nodes.defaults.essential.getter import GetterNodeTemplate
from cvp.nodes.defaults.essential.logging import LoggingNodeTemplate
from cvp.nodes.defaults.essential.setter import SetterNodeTemplate
from cvp.nodes.template import NodeTemplate


@lru_cache
def get_essential_types() -> Sequence[Type]:
    return (
        EntrypointNodeTemplate,
        LoggingNodeTemplate,
        GetterNodeTemplate,
        SetterNodeTemplate,
    )


@lru_cache
def get_essential_nodes() -> Sequence[NodeTemplate]:
    return tuple(cls() for cls in get_essential_types())
