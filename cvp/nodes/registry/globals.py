# -*- coding: utf-8 -*-

from functools import lru_cache

from cvp.nodes.registry.registry import NodeRegistry
from cvp.patterns.singleton import singleton


@singleton
class GlobalNodeRegistry(NodeRegistry):
    pass


@lru_cache
def global_node_registry() -> GlobalNodeRegistry:
    return GlobalNodeRegistry()


def register_node():
    return global_node_registry().register()
