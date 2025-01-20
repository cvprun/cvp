# -*- coding: utf-8 -*-

from typing import Optional, Sequence

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.defaults.essential.entrypoint import EntrypointNodeTemplate
from cvp.nodes.defaults.essential.logging import LoggingNodeTemplate
from cvp.nodes.node import Node


def get_essential_nodes(
    dtype_registry: Optional[DtypeRegistry] = None,
) -> Sequence[Node]:
    dtype_registry = dtype_registry if dtype_registry else global_dtype_registry()
    assert dtype_registry is not None

    return (
        EntrypointNodeTemplate(dtype_registry),
        LoggingNodeTemplate(dtype_registry),
    )
