# -*- coding: utf-8 -*-

from typing import Optional, Sequence

from cvp.pins.action import Action
from cvp.pins.kind import PinKind
from cvp.pins.stream import Stream
from cvp.pins.template import PinTemplate


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
            hidden=False,
            arcs=arcs,
            kind=PinKind.flow_only,
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
            hidden=False,
            arcs=arcs,
            kind=PinKind.flow_only,
        )
