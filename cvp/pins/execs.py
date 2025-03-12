# -*- coding: utf-8 -*-

from typing import Iterable, Optional

from cvp.pins.action import Action
from cvp.pins.kind import PinKind
from cvp.pins.stream import Stream
from cvp.pins.template import PinName, PinTemplate, WireKey


class ExecInputPinTemplate(PinTemplate):
    def __init__(
        self,
        name: PinName,
        docs: Optional[str] = None,
        wires: Optional[Iterable[WireKey]] = None,
    ):
        super().__init__(
            name=name,
            dtype=None,
            docs=docs,
            action=Action.exec,
            stream=Stream.input,
            required=False,
            hidden=False,
            wires=wires,
            kind=PinKind.exec_only,
        )


class ExecOutputPinTemplate(PinTemplate):
    def __init__(
        self,
        name: PinName,
        docs: Optional[str] = None,
        wires: Optional[Iterable[WireKey]] = None,
    ):
        super().__init__(
            name=name,
            dtype=None,
            docs=docs,
            action=Action.exec,
            stream=Stream.output,
            required=False,
            hidden=False,
            wires=wires,
            kind=PinKind.exec_only,
        )
