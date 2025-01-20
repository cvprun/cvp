# -*- coding: utf-8 -*-

from typing import Optional, Sequence

from cvp.dtypes.registry.globals import global_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.catalog.defaults.entrypoint import EntrypointNodeTemplate
from cvp.nodes.catalog.defaults.logging import LoggingNodeTemplate
from cvp.nodes.node import NodeTemplate


def get_default_nodes(
    *,
    dtype_registry: Optional[DtypeRegistry] = None,
) -> Sequence[NodeTemplate]:
    dtype_registry = dtype_registry if dtype_registry else global_registry()
    assert dtype_registry is not None

    return (
        EntrypointNodeTemplate(dtype_registry),
        LoggingNodeTemplate(dtype_registry),
    )
