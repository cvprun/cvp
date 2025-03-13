# -*- coding: utf-8 -*-

from typing import Iterable, Optional

from cvp.dtypes.dtype import Dtype
from cvp.inspect.parameter import NoDefault
from cvp.pins.action import Action
from cvp.pins.kind import PinKind
from cvp.pins.stream import Stream
from cvp.pins.template import PinName, PinTemplate, WireKey


class DataInputPinTemplate(PinTemplate):
    def __init__(
        self,
        name: PinName,
        dtype: Dtype,
        docs: Optional[str] = None,
        required=False,
        hidden=False,
        wires: Optional[Iterable[WireKey]] = None,
        kind=PinKind.unknown,
        default=NoDefault,
    ):
        super().__init__(
            name=name,
            dtype=dtype,
            action=Action.data,
            stream=Stream.input,
            docs=docs,
            required=required,
            hidden=hidden,
            wires=wires,
            kind=kind,
            default=default,
        )


class DataOutputPinTemplate(PinTemplate):
    def __init__(
        self,
        name: PinName,
        dtype: Dtype,
        docs: Optional[str] = None,
        hidden=False,
        wires: Optional[Iterable[WireKey]] = None,
        kind=PinKind.unknown,
        default=NoDefault,
    ):
        super().__init__(
            name=name,
            dtype=dtype,
            action=Action.data,
            stream=Stream.output,
            docs=docs,
            required=False,
            hidden=hidden,
            wires=wires,
            kind=kind,
            default=default,
        )
