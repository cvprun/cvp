# -*- coding: utf-8 -*-

from functools import lru_cache
from typing import Optional, Sequence

from cvp.flow.registry.registry import FlowRegistry
from cvp.flow.templates.pin import PinTemplate
from cvp.patterns.singleton import singleton
from cvp.types.colors import RGBA


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
    return global_registry().register_node(
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
