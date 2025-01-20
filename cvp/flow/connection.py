# -*- coding: utf-8 -*-

from typing import NamedTuple

from cvp.flow.node_pin import FlowNodePin
from cvp.variables import FLOW_PATH_SEPARATOR


class FlowConnection(NamedTuple):
    output: FlowNodePin
    input: FlowNodePin

    def __str__(self):
        return f"{self.output}{FLOW_PATH_SEPARATOR}{self.input}"
