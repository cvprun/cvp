# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List
from uuid import uuid4

from cvp.flow.datas.templates.pin import PinTemplate
from cvp.types.colors import RGBA, WHITE_RGBA


@dataclass
class NodeTemplate:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = str()
    docs: str = str()
    icon: str = str()
    color: RGBA = WHITE_RGBA
    pins: List[PinTemplate] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

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
