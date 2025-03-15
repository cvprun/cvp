# -*- coding: utf-8 -*-

from typing import Iterable, Optional

from cvp.inspect.parameter import NoDefault
from cvp.pins.action import Action
from cvp.pins.kind import PinKind
from cvp.pins.pin import Pin, PinName, WireKey
from cvp.pins.stream import Stream
from cvp.variables import NODOC


class ExecInputPin(Pin):
    def __init__(
        self,
        name: PinName,
        docs=NODOC,
        wires: Optional[Iterable[WireKey]] = None,
    ):
        super().__init__(
            name=name,
            dtype=None,
            action=Action.exec,
            stream=Stream.input,
            kind=PinKind.exec_only,
            default=NoDefault,
            docs=docs,
            wires=wires,
            required=False,
            hidden=False,
        )


class ExecOutputPin(Pin):
    def __init__(
        self,
        name: PinName,
        docs=NODOC,
        wire: Optional[WireKey] = None,
    ):
        super().__init__(
            name=name,
            dtype=None,
            action=Action.exec,
            stream=Stream.output,
            kind=PinKind.exec_only,
            default=NoDefault,
            docs=docs,
            wires=(wire,) if wire else None,
            required=False,
            hidden=False,
        )
