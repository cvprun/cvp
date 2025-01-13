# -*- coding: utf-8 -*-

from typing import Any, Callable, List, Optional

from cvp.flow.templates.pin import PinTemplate
from cvp.types.colors import RGBA, WHITE_RGBA


class NodeTemplate:
    def __init__(
        self,
        name: str,
        path: str,
        func: Optional[Callable] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
        pins: Optional[List[PinTemplate]] = None,
        tags: Optional[List[str]] = None,
    ):
        self.name = name
        self.path = path
        self.func = func
        self.docs = docs if docs else str()
        self.icon = icon if icon else str()
        self.color = color if color else WHITE_RGBA
        self.pins = list(pins if pins else [])
        self.tags = list(tags if tags else [])

    def __call__(self, *args, **kwargs) -> Any:
        return self.func(*args, **kwargs)

    @property
    def flow_inputs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_flow_inputs, self.pins))

    @property
    def flow_outputs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_flow_outputs, self.pins))

    @property
    def data_inputs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_data_inputs, self.pins))

    @property
    def data_outputs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_data_outputs, self.pins))
