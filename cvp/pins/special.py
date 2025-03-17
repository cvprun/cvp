# -*- coding: utf-8 -*-

from typing import (
    Annotated,
    Any,
    Final,
    Union,
    get_args,
    get_origin,
)

from cvp.dtypes.dtype import Dtype
from cvp.pins.datas import DataOutputPin
from cvp.pins.execs import ExecInputPin, ExecOutputPin
from cvp.pins.kind import PinKind
from cvp.pins.pin import PinName

ENTRYPOINT_PIN_NAME: Final[PinName] = PinName("entrypoint")
ENTRYPOINT_PIN_DOCS: Final[str] = "Indicates the starting point of the flow"

PREV_PIN_NAME: Final[PinName] = PinName("prev")
PREV_PIN_DOCS: Final[str] = "Marks the starting point of a generic function"

NEXT_PIN_NAME: Final[PinName] = PinName("next")
NEXT_PIN_DOCS: Final[str] = "Marks the endpoint of a generic function"

EMPTY_NEXT_PIN_NAME: Final[PinName] = PinName(str())
EMPTY_NEXT_PIN_DOCS: Final[str] = "None next pin"

RETURN_PIN_NAME: Final[PinName] = PinName("return")
RETURN_PIN_DOCS: Final[str] = "The return value of a function"


class EntrypointPin(ExecOutputPin):
    def __init__(self):
        super().__init__(ENTRYPOINT_PIN_NAME, ENTRYPOINT_PIN_DOCS)


class PrevPin(ExecInputPin):
    def __init__(self):
        super().__init__(PREV_PIN_NAME, PREV_PIN_DOCS)


class NextPin(ExecOutputPin):
    def __init__(self):
        super().__init__(NEXT_PIN_NAME, NEXT_PIN_DOCS)


class EmptyNextPin(ExecOutputPin):
    def __init__(self):
        super().__init__(EMPTY_NEXT_PIN_NAME, EMPTY_NEXT_PIN_DOCS)


class ReturnPin(DataOutputPin):
    def __init__(self, dtype: Dtype):
        super().__init__(
            name=RETURN_PIN_NAME,
            dtype=dtype,
            docs=RETURN_PIN_DOCS,
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
        else:
            return_dtype = Dtype(return_annotation)

        return cls(return_dtype)
