# -*- coding: utf-8 -*-

from typing import Any, Optional, Sequence

from cvp.dtypes.dtype import Dtype
from cvp.pins.datas import DataOutputPin
from cvp.pins.flows import FlowInputPin, FlowOutputPin
from cvp.pins.markers import NoDefault


class EntrypointPin(FlowInputPin):
    def __init__(self, arcs: Optional[Sequence[str]] = None):
        super().__init__(
            name="entrypoint",
            docs="Indicates the starting point of the flow",
            arcs=arcs,
        )


class PrevPin(FlowInputPin):
    def __init__(self, arcs: Optional[Sequence[str]] = None):
        super().__init__(
            name="prev",
            docs="Marks the starting point of a generic function",
            arcs=arcs,
        )


class NextPin(FlowOutputPin):
    def __init__(self, arcs: Optional[Sequence[str]] = None):
        super().__init__(
            name="next",
            docs="Marks the endpoint of a generic function",
            arcs=arcs,
        )


class ReturnPin(DataOutputPin):
    def __init__(
        self,
        dtype: Optional[Dtype] = None,
        arcs: Optional[Sequence[str]] = None,
        default: Any = NoDefault,
    ):
        super().__init__(
            name="return",
            dtype=dtype,
            docs="The return value of a function",
            arcs=arcs,
            default=default,
        )
