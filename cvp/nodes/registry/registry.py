# -*- coding: utf-8 -*-

from typing import Callable, Dict, Iterable, Optional, Union

from cvp.fonts.types import IconCode
from cvp.nodes.defaults import get_default_path2nodes
from cvp.nodes.defaults.essential.getter import GetterNode
from cvp.nodes.defaults.essential.setter import SetterNode
from cvp.nodes.node import Node, NodeName, NodePath
from cvp.pins.pin import Pin
from cvp.types.colors import RGBA


class NodeRegistry:
    _nodes: Dict[str, Node]

    def __init__(self, *, no_defaults=False):
        self._nodes = dict()
        self._getter_node = GetterNode()
        self._setter_node = SetterNode()

        if not no_defaults:
            self._nodes.update(get_default_path2nodes())

    @property
    def nodes(self):
        return self._nodes

    @property
    def getter_node(self):
        return self._getter_node

    @property
    def setter_node(self):
        return self._setter_node

    def keys(self):
        return self._nodes.keys()

    def values(self):
        return self._nodes.values()

    def items(self):
        return self._nodes.items()

    def clear(self) -> None:
        self._nodes.clear()

    def update(self, other: "NodeRegistry") -> None:
        self._nodes.update(other._nodes)

    def has(self, path: Union[str, Node]) -> bool:
        if isinstance(path, Node):
            return path.path in self._nodes
        elif isinstance(path, str):
            return path in self._nodes
        else:
            raise TypeError(f"Unsupported path type: {type(path).__name__}")

    def get(self, path: Union[str, Node]) -> Node:
        if isinstance(path, Node):
            return self._nodes[path.path]
        elif isinstance(path, str):
            return self._nodes[path]
        else:
            raise TypeError(f"Unsupported path type: {type(path).__name__}")

    def __len__(self) -> int:
        return len(self._nodes)

    def __contains__(self, path: Union[str, Node]) -> bool:
        return self.has(path)

    def __getitem__(self, path: Union[str, Node]) -> Node:
        return self.get(path)

    def add(self, node: Node) -> None:
        if node.path in self._nodes:
            raise KeyError(f"Duplicate node path: {node.path}")
        self._nodes[node.path] = node

    def add_new(
        self,
        func: Callable,
        path: Optional[NodePath] = None,
        name: Optional[NodeName] = None,
        docs: Optional[str] = None,
        icon: Optional[IconCode] = None,
        color: Optional[RGBA] = None,
        exec_inputs: Optional[Iterable[Pin]] = None,
        exec_outputs: Optional[Iterable[Pin]] = None,
        data_inputs: Optional[Iterable[Pin]] = None,
        data_outputs: Optional[Iterable[Pin]] = None,
        tags: Optional[Iterable[str]] = None,
    ) -> Node:
        node = Node.from_callable(
            func=func,
            path=path,
            name=name,
            docs=docs,
            icon=icon,
            color=color,
            exec_inputs=exec_inputs,
            exec_outputs=exec_outputs,
            data_inputs=data_inputs,
            data_outputs=data_outputs,
            tags=tags,
        )
        self.add(node)
        return node

    def register(
        self,
        name: Optional[NodeName] = None,
        path: Optional[NodePath] = None,
        docs: Optional[str] = None,
        icon: Optional[IconCode] = None,
        color: Optional[RGBA] = None,
        exec_inputs: Optional[Iterable[Pin]] = None,
        exec_outputs: Optional[Iterable[Pin]] = None,
        data_inputs: Optional[Iterable[Pin]] = None,
        data_outputs: Optional[Iterable[Pin]] = None,
        tags: Optional[Iterable[str]] = None,
    ):
        def _decorator(func: Callable):
            self.add_new(
                func=func,
                path=path,
                name=name,
                docs=docs,
                icon=icon,
                color=color,
                exec_inputs=exec_inputs,
                exec_outputs=exec_outputs,
                data_inputs=data_inputs,
                data_outputs=data_outputs,
                tags=tags,
            )
            return func

        return _decorator
