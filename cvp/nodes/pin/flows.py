# -*- coding: utf-8 -*-

from typing import Optional, Sequence

from cvp.nodes.action import Action
from cvp.nodes.pin.pin import PinTemplate
from cvp.nodes.stream import Stream


class FlowInputPinTemplate(PinTemplate):
    def __init__(
        self,
        name: str,
        docs: Optional[str] = None,
        arcs: Optional[Sequence[str]] = None,
    ):
        super().__init__(
            name=name,
            dtype=None,
            docs=docs,
            action=Action.flow,
            stream=Stream.input,
            required=False,
            arcs=arcs,
        )


class FlowOutputPinTemplate(PinTemplate):
    def __init__(
        self,
        name: str,
        docs: Optional[str] = None,
        arcs: Optional[Sequence[str]] = None,
    ):
        super().__init__(
            name=name,
            dtype=None,
            docs=docs,
            action=Action.flow,
            stream=Stream.output,
            required=False,
            arcs=arcs,
        )
