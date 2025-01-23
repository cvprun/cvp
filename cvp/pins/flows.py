# -*- coding: utf-8 -*-

from typing import Optional, Sequence

from cvp.pins.action import Action
from cvp.pins.kind import PinKind
from cvp.pins.pin import Pin
from cvp.pins.stream import Stream


class FlowInputPin(Pin):
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
            kind=PinKind.flow_only,
        )


class FlowOutputPin(Pin):
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
            kind=PinKind.flow_only,
        )
