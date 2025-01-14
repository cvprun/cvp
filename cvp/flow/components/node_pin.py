# -*- coding: utf-8 -*-

from typing import NamedTuple

from cvp.flow.components.node import Node
from cvp.flow.components.pin import Pin
from cvp.flow.components.prefix import Prefix


class NodePin(NamedTuple):
    node: Node
    pin: Pin

    def __str__(self):
        return f"{self.node.name}{Prefix.pin.value}{self.pin.name}"
