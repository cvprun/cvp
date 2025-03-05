# -*- coding: utf-8 -*-

from typing import Optional, Sequence

from cvp.pins.action import Action
from cvp.pins.kind import PinKind
from cvp.pins.stream import Stream
from cvp.pins.template import PinTemplate


class ExecInputPinTemplate(PinTemplate):
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
            action=Action.exec,
            stream=Stream.input,
            required=False,
            hidden=False,
            arcs=arcs,
            kind=PinKind.exec_only,
        )


class ExecOutputPinTemplate(PinTemplate):
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
            action=Action.exec,
            stream=Stream.output,
            required=False,
            hidden=False,
            arcs=arcs,
            kind=PinKind.exec_only,
        )
