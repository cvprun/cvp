# -*- coding: utf-8 -*-

from functools import lru_cache
from types import MappingProxyType

from cvp.flow.templates.node import NodeTemplate

NodeMapping = MappingProxyType[str, NodeTemplate]


@lru_cache
def get_default_nodes() -> NodeMapping:
    return NodeMapping({})
