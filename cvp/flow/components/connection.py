# -*- coding: utf-8 -*-

from typing import NamedTuple

from cvp.flow.components.node_pin import NodePin
from cvp.flow.components.prefix import Prefix


class Connection(NamedTuple):
    output: NodePin
    input: NodePin

    def __str__(self):
        return f"{self.output}{Prefix.arc.value}{self.input}"
