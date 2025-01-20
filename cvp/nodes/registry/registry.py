# -*- coding: utf-8 -*-

from typing import Callable, Dict, Optional, Sequence

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults import get_default_nodes
from cvp.nodes.node import Node
from cvp.pins.pin import Pin
from cvp.types.colors import RGBA


class NodeRegistry:
    _path2dtypes: Dict[str, Dtype]
    _type2dtypes: Dict[type, Dtype]
    _nodes: Dict[str, Node]

    def __init__(self, *, no_defaults=False):
        self._path2dtypes = dict()
        self._type2dtypes = dict()
        self._nodes = dict()

        if not no_defaults:
            self.register_default_nodes()

    def register_default_nodes(self) -> None:
        for node in get_default_nodes().values():
            self.add_node(node)

    @property
    def nodes(self):
        return self._nodes

    def update(self, other: "NodeRegistry") -> None:
        self._nodes.update(other.nodes)

    def add_node(self, node: Node) -> None:
        if node.path in self._nodes:
            raise KeyError(f"Duplicate node path: {node.path}")
        self._nodes[node.path] = node

    def add_new_callable(
        self,
        func: Callable,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
        flow_inputs: Optional[Sequence[Pin]] = None,
        flow_outputs: Optional[Sequence[Pin]] = None,
        data_inputs: Optional[Sequence[Pin]] = None,
        data_outputs: Optional[Sequence[Pin]] = None,
        tags: Optional[Sequence[str]] = None,
    ):
        node = Node.from_grouped_pins(
            func=func,
            name=name,
            path=path,
            docs=docs,
            icon=icon,
            color=color,
            flow_inputs=flow_inputs,
            flow_outputs=flow_outputs,
            data_inputs=data_inputs,
            data_outputs=data_outputs,
            tags=tags,
        )
        self.add_node(node)

    def register_node(
        self,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
        flow_inputs: Optional[Sequence[Pin]] = None,
        flow_outputs: Optional[Sequence[Pin]] = None,
        data_inputs: Optional[Sequence[Pin]] = None,
        data_outputs: Optional[Sequence[Pin]] = None,
        tags: Optional[Sequence[str]] = None,
    ):
        def _decorator(func: Callable):
            self.add_new_callable(
                func=func,
                name=name,
                path=path,
                docs=docs,
                icon=icon,
                color=color,
                flow_inputs=flow_inputs,
                flow_outputs=flow_outputs,
                data_inputs=data_inputs,
                data_outputs=data_outputs,
                tags=tags,
            )
            return func

        return _decorator
