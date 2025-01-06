# -*- coding: utf-8 -*-

from typing import NamedTuple

from cvp.flow.datas.node_pin import NodePin
from cvp.flow.datas.prefix import Prefix


class Connection(NamedTuple):
    output: NodePin
    input: NodePin

    def __str__(self):
        return f"{self.output}{Prefix.arc.value}{self.input}"
