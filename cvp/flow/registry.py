# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Any, Dict, Optional, Union

from cvp.flow.builtins.dtype import get_builtin_dtypes
from cvp.flow.builtins.node import get_builtin_nodes
from cvp.flow.icons.dtype import DTYPE_ICON_MAPPING
from cvp.flow.templates.dtype import Dtype
from cvp.flow.templates.node import NodeTemplate
from cvp.patterns.singleton import singleton
from cvp.types.colors import RGBA, WHITE_RGBA
from cvp.variables import FLOW_PATH_SEPARATOR


class FlowRegistry:
    _dtypes: Dict[str, Dtype]
    _type2dtypes: Dict[type, Dtype]
    _nodes: Dict[str, NodeTemplate]

    def __init__(self, *, no_builtins=False):
        self._dtypes = dict()
        self._type2dtypes = dict()
        self._nodes = dict()

        if not no_builtins:
            self.register_builtin_nodes()
            self.register_builtin_dtypes()

    def register_builtin_nodes(self) -> None:
        for dtype in get_builtin_dtypes():
            self.add_dtype(dtype)

    def register_builtin_dtypes(self) -> None:
        for node in get_builtin_nodes():
            self.add_node(node)

    @property
    def dtypes(self):
        return self._dtypes

    @property
    def type2dtypes(self):
        return self._type2dtypes

    @property
    def nodes(self):
        return self._nodes

    @staticmethod
    def create_dtype(
        base: Any,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
    ) -> Dtype:
        if not isinstance(base, type):
            raise TypeError(f"Only types can be registered: {base}")

        base_name = name if name else base.__name__
        base_path = path if path else base.__module__ + FLOW_PATH_SEPARATOR + base_name
        base_docs = docs if docs else base.__doc__
        base_icon = icon if icon else DTYPE_ICON_MAPPING[base_name[0]]
        base_color = color if color else WHITE_RGBA

        if not base_name:
            raise ValueError("The 'name' attribute is required")
        if not base_path:
            raise ValueError("The 'path' attribute is required")

        return Dtype(
            name=base_name,
            path=base_path,
            base=base,
            docs=base_docs,
            icon=base_icon,
            color=base_color,
        )

    def add_dtype(self, dtype: Dtype) -> None:
        if dtype.path in self._dtypes:
            raise KeyError(f"Duplicate dtype path: {dtype.path}")
        self._dtypes[dtype.path] = dtype
        self._type2dtypes[dtype.base] = dtype

    def add_node(self, node: NodeTemplate) -> None:
        if node.path in self._nodes:
            raise KeyError(f"Duplicate node path: {node.path}")
        self._nodes[node.path] = node

    def register(self, item: Union[Dtype, NodeTemplate]):
        if isinstance(item, Dtype):
            self.add_dtype(item)
        elif isinstance(item, NodeTemplate):
            self.add_node(item)
        else:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

    def register_dtype(
        self,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
    ):
        def _decorator(base: Any):
            dtype = self.create_dtype(
                base,
                name=name,
                path=path,
                docs=docs,
                icon=icon,
                color=color,
            )
            self.add_dtype(dtype)

        return _decorator

    def update(self, other: "FlowRegistry") -> None:
        self._dtypes.update(other.dtypes)
        self._nodes.update(other.nodes)


@singleton
class GlobalFlowRegistry(FlowRegistry):
    pass


@lru_cache
def global_registry() -> GlobalFlowRegistry:
    return GlobalFlowRegistry()


def register_dtype(
    name: Optional[str] = None,
    path: Optional[str] = None,
    docs: Optional[str] = None,
    icon: Optional[str] = None,
    color: Optional[RGBA] = None,
):
    return global_registry().register_dtype(
        name=name,
        path=path,
        docs=docs,
        icon=icon,
        color=color,
    )
