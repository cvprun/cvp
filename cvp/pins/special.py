# -*- coding: utf-8 -*-

from typing import (
    Annotated,
    Any,
    Final,
    Iterable,
    Optional,
    Union,
    get_args,
    get_origin,
)

from cvp.dtypes.dtype import Dtype
from cvp.pins.annotated import get_wires
from cvp.pins.datas import DataOutputPin
from cvp.pins.execs import ExecInputPin, ExecOutputPin
from cvp.pins.kind import PinKind
from cvp.pins.pin import PinName, WireKey

ENTRYPOINT_PIN_NAME: Final[PinName] = PinName("entrypoint")
ENTRYPOINT_PIN_DOCS: Final[str] = "Indicates the starting point of the flow"

PREV_PIN_NAME: Final[PinName] = PinName("prev")
PREV_PIN_DOCS: Final[str] = "Marks the starting point of a generic function"

NEXT_PIN_NAME: Final[PinName] = PinName("next")
NEXT_PIN_DOCS: Final[str] = "Marks the endpoint of a generic function"

RETURN_PIN_NAME: Final[PinName] = PinName("return")
RETURN_PIN_DOCS: Final[str] = "The return value of a function"


class EntrypointPin(ExecOutputPin):
    def __init__(self, wire: Optional[WireKey] = None):
        super().__init__(
            name=ENTRYPOINT_PIN_NAME,
            docs=ENTRYPOINT_PIN_DOCS,
            wire=wire,
        )


class PrevPin(ExecInputPin):
    def __init__(self, wires: Optional[Iterable[WireKey]] = None):
        super().__init__(
            name=PREV_PIN_NAME,
            docs=PREV_PIN_DOCS,
            wires=wires,
        )


class NextPin(ExecOutputPin):
    def __init__(self, wire: Optional[WireKey] = None):
        super().__init__(
            name=NEXT_PIN_NAME,
            docs=NEXT_PIN_DOCS,
            wire=wire,
        )


class ReturnPin(DataOutputPin):
    def __init__(
        self,
        dtype: Dtype,
        wires: Optional[Iterable[WireKey]] = None,
    ):
        super().__init__(
            name=RETURN_PIN_NAME,
            dtype=dtype,
            docs=RETURN_PIN_DOCS,
            wires=wires,
            kind=PinKind.return_only,
        )

    @classmethod
    def from_return_annotation(cls, return_annotation: Any):
        return_origin = get_origin(return_annotation)
        if return_origin == Union:
            raise TypeError("Union return is not supported")

        if return_origin == Annotated:
            return_args = get_args(return_annotation)
            assert 2 <= len(return_args)
            return_dtype = Dtype(return_args[0])  # type: ignore[var-annotated]
            return_wires = list(WireKey(w) for w in get_wires(*return_args))
        else:
            return_dtype = Dtype(return_annotation)
            return_wires = list()

        return cls(return_dtype, return_wires)
