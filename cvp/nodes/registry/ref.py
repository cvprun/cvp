# -*- coding: utf-8 -*-

from typing import Optional
from weakref import ReferenceType, ref

from cvp.nodes.registry.globals import global_node_registry
from cvp.nodes.registry.registry import NodeRegistry


class NodeRegistryRef:
    _ref: ReferenceType[NodeRegistry]

    def __init__(self, node_registry: Optional[NodeRegistry] = None):
        if node_registry is None:
            node_registry = global_node_registry()
        assert node_registry is not None
        self._ref = ref(node_registry)

    def get(self) -> Optional[NodeRegistry]:
        return self._ref()

    @staticmethod
    def get_global() -> NodeRegistry:
        return global_node_registry()

    def get_force(self) -> NodeRegistry:
        if registry := self.get():
            return registry
        else:
            return global_node_registry()

    def __call__(self) -> NodeRegistry:
        return self.get_force()
