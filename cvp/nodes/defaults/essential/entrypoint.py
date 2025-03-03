# -*- coding: utf-8 -*-

from typing import Optional

from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.fonts.glyphs.mdi import PLAY
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.flows import FlowOutputPin
from cvp.pins.pin import Pin
from cvp.types.colors import GREEN_RGBA
from cvp.types.override import override


class EntrypointNode(Node):
    def __init__(self, _: DtypeRegistry):
        self._start = FlowOutputPin(
            name="start",
            docs="Entrypoint flow signal",
        )
        super().__init__(
            name="Entrypoint",
            path="cvp.essential.entrypoint",
            func=None,
            docs="Indicates the starting point of the graph",
            icon=PLAY,
            color=GREEN_RGBA,
            pins=(self._start,),
            tags=("entrypoint", "main"),
        )

    @override
    def run(self, record: NodeRecord) -> Optional[Pin]:
        return self._start
