# -*- coding: utf-8 -*-

from typing import Union

from cvp.dtypes.dtype import Dtype
from cvp.inspect.parameter import NoDefault
from cvp.pins.action import Action
from cvp.pins.kind import PinKind
from cvp.pins.pin import Pin, PinName
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
            required=False,
            hidden=hidden,
        )
