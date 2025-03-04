# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Optional, Sequence

from cvp.nodes.registry.registry import NodeRegistry
from cvp.patterns.singleton import singleton
from cvp.pins.template import PinTemplate
from cvp.types.colors import RGBA


@singleton
class GlobalNodeRegistry(NodeRegistry):
    pass


@lru_cache
def global_node_registry() -> GlobalNodeRegistry:
    return GlobalNodeRegistry()


def register_node(
    name: Optional[str] = None,
    path: Optional[str] = None,
    docs: Optional[str] = None,
    icon: Optional[str] = None,
    color: Optional[RGBA] = None,
    flow_inputs: Optional[Sequence[PinTemplate]] = None,
    flow_outputs: Optional[Sequence[PinTemplate]] = None,
    data_inputs: Optional[Sequence[PinTemplate]] = None,
    data_outputs: Optional[Sequence[PinTemplate]] = None,
    tags: Optional[Sequence[str]] = None,
):
    return global_node_registry().register(
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
