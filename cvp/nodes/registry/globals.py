# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Iterable, Optional

from cvp.fonts.types import IconCode
from cvp.nodes.registry.registry import NodeRegistry
from cvp.nodes.template import NodePath
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
):
    return global_node_registry().register(
        name=name,
        path=path,
        docs=docs,
        icon=icon,
        color=color,
        exec_inputs=exec_inputs,
        exec_outputs=exec_outputs,
        data_inputs=data_inputs,
        data_outputs=data_outputs,
        tags=tags,
    )
