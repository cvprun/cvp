# -*- coding: utf-8 -*-

from typing import Callable, Dict, Optional, Sequence, Union
from weakref import ReferenceType, ref

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults import get_default_path2nodes
from cvp.nodes.node import Node
from cvp.pins.pin import Pin
from cvp.types.colors import RGBA


class NodeRegistry:
    _dtype_registry: ReferenceType[DtypeRegistry]
    _nodes: Dict[str, Node]

    def __init__(
        self,
        dtype_registry: Optional[DtypeRegistry] = None,
        *,
        no_defaults=False,
    ):
        if dtype_registry is None:
            dtype_registry = global_dtype_registry()
        assert dtype_registry is not None
        self._dtype_registry = ref(dtype_registry)
        self._nodes = dict()

        if not no_defaults:
            self._nodes.update(get_default_path2nodes(dtype_registry))

    @property
    def nodes(self):
        return self._nodes

    @property
    def dtype_registry(self) -> Optional[DtypeRegistry]:
        return self._dtype_registry()

    def keys(self):
        return self._nodes.keys()

    def values(self):
        return self._nodes.values()

    def items(self):
        return self._nodes.items()

    def clear(self) -> None:
        self._nodes.clear()

    def update(self, other: "NodeRegistry") -> None:
        self._nodes.update(other.nodes)

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
    ) -> Node:
        node = Node.auto_parse(
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
            dtype_registry=self.dtype_registry,
        )
        self.add(node)
        return node

    def register(
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
            self.add_new(
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
