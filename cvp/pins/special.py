# -*- coding: utf-8 -*-

from typing import Any, Optional, Sequence

from cvp.pins.datas import DataOutputPinTemplate
from cvp.pins.flows import FlowInputPinTemplate, FlowOutputPinTemplate
from cvp.pins.markers import NoDefault


class EntrypointPinTemplate(FlowInputPinTemplate):
    def __init__(self, arcs: Optional[Sequence[str]] = None):
        super().__init__(
            name="entrypoint",
            docs="Indicates the starting point of the flow",
            arcs=arcs,
        )


class PrevPinTemplate(FlowInputPinTemplate):
    def __init__(self, arcs: Optional[Sequence[str]] = None):
        super().__init__(
            name="prev",
            docs="Marks the starting point of a generic function",
            arcs=arcs,
        )


class NextPinTemplate(FlowOutputPinTemplate):
    def __init__(self, arcs: Optional[Sequence[str]] = None):
        super().__init__(
            name="next",
            docs="Marks the endpoint of a generic function",
            arcs=arcs,
        )


class ReturnPinTemplate(DataOutputPinTemplate):
    def __init__(
        self,
        dtype: Optional[str] = None,
        required: Optional[bool] = None,
        arcs: Optional[Sequence[str]] = None,
        default: Any = NoDefault,
    ):
        super().__init__(
            name="return",
            dtype=dtype,
            docs="The return value of a function",
            required=required,
            arcs=arcs,
            default=default,
        )
