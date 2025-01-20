# -*- coding: utf-8 -*-

from typing import Any, Optional, Sequence

from cvp.dtypes.dtype import Dtype
from cvp.pins.action import Action
from cvp.pins.markers import NoDefault
from cvp.pins.pin import Pin
from cvp.pins.stream import Stream


class DataInputPin(Pin):
    def __init__(
        self,
        name: str,
        dtype: Optional[Dtype] = None,
        docs: Optional[str] = None,
        required: Optional[bool] = None,
        arcs: Optional[Sequence[str]] = None,
        default: Any = NoDefault,
    ):
        super().__init__(
            name=name,
            dtype=dtype,
            docs=docs,
            action=Action.data,
            stream=Stream.input,
            required=required,
            arcs=arcs,
            default=default,
        )


class DataOutputPin(Pin):
    def __init__(
        self,
        name: str,
        dtype: Optional[Dtype] = None,
        docs: Optional[str] = None,
        arcs: Optional[Sequence[str]] = None,
        default: Any = NoDefault,
    ):
        super().__init__(
            name=name,
            dtype=dtype,
            docs=docs,
            action=Action.data,
            stream=Stream.output,
            required=False,
            arcs=arcs,
            default=default,
        )
