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
from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.pins.annotated import get_docs, get_name, get_wires
from cvp.pins.datas import DataOutputPinTemplate
from cvp.pins.execs import ExecInputPinTemplate, ExecOutputPinTemplate
from cvp.pins.kind import PinKind
from cvp.pins.template import PinName, WireKey

ENTRYPOINT_PIN_NAME: Final[PinName] = PinName("entrypoint")
ENTRYPOINT_PIN_DOCS: Final[str] = "Indicates the starting point of the flow"

PREV_PIN_NAME: Final[PinName] = PinName("prev")
PREV_PIN_DOCS: Final[str] = "Marks the starting point of a generic function"

NEXT_PIN_NAME: Final[PinName] = PinName("next")
NEXT_PIN_DOCS: Final[str] = "Marks the endpoint of a generic function"

RETURN_PIN_NAME: Final[PinName] = PinName("return")
RETURN_PIN_DOCS: Final[str] = "The return value of a function"


class EntrypointPinTemplate(ExecInputPinTemplate):
    def __init__(
        self,
        name: Optional[PinName] = None,
        docs: Optional[str] = None,
        wires: Optional[Iterable[WireKey]] = None,
    ):
        super().__init__(
            name=name if name else ENTRYPOINT_PIN_NAME,
            docs=docs if docs else ENTRYPOINT_PIN_DOCS,
            wires=wires,
        )


class PrevPinTemplate(ExecInputPinTemplate):
    def __init__(
        self,
        name: Optional[PinName] = None,
        docs: Optional[str] = None,
        wires: Optional[Iterable[WireKey]] = None,
    ):
        super().__init__(
            name=name if name else PREV_PIN_NAME,
            docs=docs if docs else PREV_PIN_DOCS,
            wires=wires,
        )


class NextPinTemplate(ExecOutputPinTemplate):
    def __init__(
        self,
        name: Optional[PinName] = None,
        docs: Optional[str] = None,
        wires: Optional[Iterable[WireKey]] = None,
    ):
        super().__init__(
            name=name if name else NEXT_PIN_NAME,
            docs=docs if docs else NEXT_PIN_DOCS,
            wires=wires,
        )


class ReturnPinTemplate(DataOutputPinTemplate):
    def __init__(
        self,
        dtype: Dtype,
        docs: Optional[str] = None,
        wires: Optional[Iterable[WireKey]] = None,
        *,
        name: Optional[PinName] = None,
    ):
        super().__init__(
            name=name if name else RETURN_PIN_NAME,
            dtype=dtype,
            docs=docs if docs else RETURN_PIN_DOCS,
            wires=wires,
            kind=PinKind.return_only,
        )

    @classmethod
    def from_return_annotation(
        cls,
        return_annotation: Any,
        *,
        dtype_registry: Optional[DtypeRegistry] = None,
    ):
        if dtype_registry is None:
            dtype_registry = global_dtype_registry()
        assert dtype_registry is not None

        return_origin = get_origin(return_annotation)
        if return_origin == Union:
            raise TypeError("Union return is not supported")

        if return_origin == Annotated:
            return_args = get_args(return_annotation)
            assert 2 <= len(return_args)
            return_dtype = dtype_registry.get(return_args[0])
            return_name = PinName(get_name(*return_args, default=RETURN_PIN_NAME))
            return_docs = get_docs(*return_args, default=RETURN_PIN_DOCS)
            return_wires = list(WireKey(w) for w in get_wires(*return_args))
        else:
            return_dtype = dtype_registry.get(return_annotation)
            return_name = RETURN_PIN_NAME
            return_docs = RETURN_PIN_DOCS
            return_wires = list()

        return cls(
            dtype=return_dtype,
            docs=return_docs,
            wires=return_wires,
            name=return_name,
        )
