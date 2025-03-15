# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Iterable, Optional

from cvp.nodes.node import NodeName, NodePath
from cvp.nodes.registry.registry import NodeRegistry
from cvp.patterns.singleton import singleton


@singleton
class GlobalNodeRegistry(NodeRegistry):
    pass


@lru_cache
def global_node_registry() -> GlobalNodeRegistry:
    return GlobalNodeRegistry()


def register_node(
    path: Optional[NodePath] = None,
    name: Optional[NodeName] = None,
    docs: Optional[str] = None,
    tags: Optional[Iterable[str]] = None,
):
    return global_node_registry().register(
        name=name,
        path=path,
        docs=docs,
        tags=tags,
    )
