# -*- coding: utf-8 -*-

from typing import Callable, Dict, Iterable, Optional, Union

from cvp.dtypes.registry.ref import DtypeRegistryRef
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.fonts.types import IconCode
from cvp.nodes.defaults import get_default_path2nodes
from cvp.nodes.defaults.essential.getter import GetterNodeTemplate
from cvp.nodes.defaults.essential.setter import SetterNodeTemplate
from cvp.nodes.template import NodePath, NodeTemplate
from cvp.pins.template import PinTemplate
from cvp.types.colors import RGBA


class NodeRegistry:
    _nodes: Dict[str, NodeTemplate]

    def __init__(
        self,
        dtype_registry: Optional[DtypeRegistry] = None,
        *,
        no_defaults=False,
    ):
        self._dtype_registry = DtypeRegistryRef(dtype_registry)

        dtype_registry = self._dtype_registry.get_force()
        assert dtype_registry is not None

        self._nodes = dict()
        self._getter_node = GetterNodeTemplate(dtype_registry)
        self._setter_node = SetterNodeTemplate(dtype_registry)

        if not no_defaults:
            self._nodes.update(get_default_path2nodes(dtype_registry))

    @property
    def dtype_registry(self):
        return self._dtype_registry.get_force()

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

    def has(self, path: Union[str, NodeTemplate]) -> bool:
        if isinstance(path, NodeTemplate):
            return path.path in self._nodes
        elif isinstance(path, str):
            return path in self._nodes
        else:
            raise TypeError(f"Unsupported path type: {type(path).__name__}")

    def get(self, path: Union[str, NodeTemplate]) -> NodeTemplate:
        if isinstance(path, NodeTemplate):
            return self._nodes[path.path]
        elif isinstance(path, str):
            return self._nodes[path]
        else:
            raise TypeError(f"Unsupported path type: {type(path).__name__}")

    def __len__(self) -> int:
        return len(self._nodes)

    def __contains__(self, path: Union[str, NodeTemplate]) -> bool:
        return self.has(path)

    def __getitem__(self, path: Union[str, NodeTemplate]) -> NodeTemplate:
        return self.get(path)

    def add(self, node: NodeTemplate) -> None:
        if node.path in self._nodes:
            raise KeyError(f"Duplicate node path: {node.path}")
        self._nodes[node.path] = node

    def add_new(
        self,
        func: Callable,
        path: Optional[NodePath] = None,
        name: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[IconCode] = None,
        color: Optional[RGBA] = None,
        exec_inputs: Optional[Iterable[PinTemplate]] = None,
        exec_outputs: Optional[Iterable[PinTemplate]] = None,
        data_inputs: Optional[Iterable[PinTemplate]] = None,
        data_outputs: Optional[Iterable[PinTemplate]] = None,
        tags: Optional[Iterable[str]] = None,
    ) -> NodeTemplate:
        node = NodeTemplate.from_callable(
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
            dtype_registry=self.dtype_registry,
        )
        self.add(node)
        return node

    def register(
        self,
        name: Optional[str] = None,
        path: Optional[NodePath] = None,
        docs: Optional[str] = None,
        icon: Optional[IconCode] = None,
        color: Optional[RGBA] = None,
        exec_inputs: Optional[Iterable[PinTemplate]] = None,
        exec_outputs: Optional[Iterable[PinTemplate]] = None,
        data_inputs: Optional[Iterable[PinTemplate]] = None,
        data_outputs: Optional[Iterable[PinTemplate]] = None,
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
