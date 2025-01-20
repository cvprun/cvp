# -*- coding: utf-8 -*-

from typing import NamedTuple

from cvp.flow.components.node import Node
from cvp.flow.components.pin import Pin
from cvp.variables import FLOW_PATH_SEPARATOR


class NodePin(NamedTuple):
    node: Node
    pin: Pin

    def __str__(self):
        return f"{self.node.name}{FLOW_PATH_SEPARATOR}{self.pin.name}"
