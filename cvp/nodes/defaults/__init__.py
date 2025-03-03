# -*- coding: utf-8 -*-

from types import MappingProxyType
from typing import List, Optional, Sequence

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults.builtins import get_builtin_nodes
from cvp.nodes.defaults.casting import get_casting_nodes
from cvp.nodes.defaults.essential import get_essential_nodes
from cvp.nodes.defaults.operators import get_operators_nodes
from cvp.nodes.node import Node

NodeMapping = MappingProxyType[str, Node]


def get_default_nodes(
    dtype_registry: Optional[DtypeRegistry] = None,
) -> Sequence[Node]:
    if dtype_registry is None:
        dtype_registry = global_dtype_registry()
    assert dtype_registry is not None
    result: List[Node] = list()
    result.extend(get_builtin_nodes(dtype_registry))
    result.extend(get_casting_nodes(dtype_registry))
    result.extend(get_essential_nodes(dtype_registry))
    result.extend(get_operators_nodes(dtype_registry))
    return tuple(result)


def get_default_path2nodes(
    dtype_registry: Optional[DtypeRegistry] = None,
) -> NodeMapping:
    return NodeMapping({node.path: node for node in get_default_nodes(dtype_registry)})
