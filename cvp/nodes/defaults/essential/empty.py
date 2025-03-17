# -*- coding: utf-8 -*-

from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.pin import Pin
from cvp.pins.special import NextPin, PrevPin
from cvp.types.override import override


class Empty(Node):
    """An empty node that does nothing"""

    def __init__(self):
        self._prev = PrevPin()
        self._next = NextPin()
        super().__init__(self._prev, self._next)

    @override
    def run(self, record: NodeRecord) -> Pin:
        return self._next
