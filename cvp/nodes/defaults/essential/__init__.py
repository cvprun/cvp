# -*- coding: utf-8 -*-

from typing import Optional, Sequence

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults.essential.entrypoint import EntrypointNode
from cvp.nodes.defaults.essential.logging import LoggingNode
from cvp.nodes.node import Node


def get_essential_nodes(
    dtype_registry: Optional[DtypeRegistry] = None,
) -> Sequence[Node]:
    if dtype_registry is None:
        dtype_registry = global_dtype_registry()
    assert dtype_registry is not None

    return (
        EntrypointNode(),
        LoggingNode(dtype_registry),
    )
