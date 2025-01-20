# -*- coding: utf-8 -*-

from typing import NamedTuple

from cvp.flow.node import FlowNode
from cvp.flow.pin import FlowPin
from cvp.variables import FLOW_PATH_SEPARATOR


class FlowNodePin(NamedTuple):
    node: FlowNode
    pin: FlowPin

    def __str__(self):
        return f"{self.node.name}{FLOW_PATH_SEPARATOR}{self.pin.name}"
