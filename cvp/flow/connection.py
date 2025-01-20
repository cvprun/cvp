# -*- coding: utf-8 -*-

from typing import NamedTuple

from cvp.flow.node_pin import NodePin
from cvp.variables import FLOW_PATH_SEPARATOR


class Connection(NamedTuple):
    output: NodePin
    input: NodePin

    def __str__(self):
        return f"{self.output}{FLOW_PATH_SEPARATOR}{self.input}"
