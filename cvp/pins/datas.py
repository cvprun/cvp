# -*- coding: utf-8 -*-

from inspect import Parameter
from typing import Any, Optional, Sequence

from cvp.pins.action import Action
from cvp.pins.pin import PinTemplate
from cvp.pins.stream import Stream


class DataInputPinTemplate(PinTemplate):
    def __init__(
        self,
        name: str,
        dtype: Optional[str] = None,
        docs: Optional[str] = None,
        required: Optional[bool] = None,
        arcs: Optional[Sequence[str]] = None,
        default: Any = Parameter.empty,
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


class DataOutputPinTemplate(PinTemplate):
    def __init__(
        self,
        name: str,
        dtype: Optional[str] = None,
        docs: Optional[str] = None,
        required: Optional[bool] = None,
        arcs: Optional[Sequence[str]] = None,
        default: Any = Parameter.empty,
    ):
        super().__init__(
            name=name,
            dtype=dtype,
            docs=docs,
            action=Action.data,
            stream=Stream.output,
            required=required,
            arcs=arcs,
            default=default,
        )
