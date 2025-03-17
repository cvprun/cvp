# -*- coding: utf-8 -*-

from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.execs import ExecOutputPin
from cvp.pins.pin import Pin, PinName
from cvp.types.override import override


class Entrypoint(Node):
    """Indicates the starting point of the graph"""

    def __init__(self):
        self._start = ExecOutputPin(
            name=PinName("start"),
            docs="Entrypoint flow signal",
        )
        super().__init__(self._start)

    @override
    def run(self, record: NodeRecord) -> Pin:
        return self._start
