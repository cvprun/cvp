# -*- coding: utf-8 -*-

from typing import Optional

from cvp.nodes.node import Node, NodeName, NodePath
from cvp.nodes.record import NodeRecord
from cvp.pins.execs import ExecOutputPin
from cvp.pins.pin import Pin, PinName
from cvp.types.override import override


class EntrypointNode(Node):
    def __init__(self):
        self._start = ExecOutputPin(
            name=PinName("start"),
            docs="Entrypoint flow signal",
        )
        super().__init__(
            path=NodePath("cvp.essential.entrypoint"),
            name=NodeName("Entrypoint"),
            func=None,
            docs="Indicates the starting point of the graph",
            pins=(self._start,),
            tags=("entrypoint", "main"),
        )

    @override
    def run(self, record: NodeRecord) -> Optional[Pin]:
        return self._start
