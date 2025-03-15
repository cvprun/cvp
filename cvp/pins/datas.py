# -*- coding: utf-8 -*-

from typing import Iterable, Optional, Union

from cvp.dtypes.dtype import Dtype
from cvp.inspect.parameter import NoDefault
from cvp.pins.action import Action
from cvp.pins.kind import PinKind
from cvp.pins.pin import Pin, PinName, WireKey
from cvp.pins.stream import Stream
from cvp.variables import NODOC


class DataInputPin(Pin):
    def __init__(
        self,
        name: PinName,
        dtype: Union[None, type, Dtype],
        kind=PinKind.positional_or_keyword,
        default=NoDefault,
        docs=NODOC,
        wire: Optional[WireKey] = None,
        *,
        required=False,
        hidden=False,
    ):
        super().__init__(
            name=name,
            dtype=dtype,
            action=Action.data,
            stream=Stream.input,
            kind=kind,
            default=default,
            docs=docs,
            wires=(wire,) if wire else None,
            required=required,
            hidden=hidden,
        )


class DataOutputPin(Pin):
    def __init__(
        self,
        name: PinName,
        dtype: Union[None, type, Dtype],
        kind=PinKind.positional_or_keyword,
        default=NoDefault,
        docs=NODOC,
        wires: Optional[Iterable[WireKey]] = None,
        *,
        hidden=False,
    ):
        super().__init__(
            name=name,
            dtype=dtype,
            action=Action.data,
            stream=Stream.output,
            kind=kind,
            default=default,
            docs=docs,
            wires=wires,
            required=False,
            hidden=hidden,
        )
