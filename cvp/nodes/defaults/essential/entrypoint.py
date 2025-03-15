# -*- coding: utf-8 -*-

from typing import Optional

from cvp.fonts.glyphs.mdi import PLAY
from cvp.nodes.record import NodeRecord
from cvp.nodes.template import NodeName, NodePath, NodeTemplate
from cvp.pins.execs import ExecOutputPin
from cvp.pins.pin import Pin, PinName
from cvp.types.colors import GREEN_RGBA
from cvp.types.override import override


class EntrypointNodeTemplate(NodeTemplate):
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
            icon=PLAY,
            color=GREEN_RGBA,
            pins=(self._start,),
            tags=("entrypoint", "main"),
        )

    @override
    def run(self, record: NodeRecord) -> Optional[Pin]:
        return self._start
