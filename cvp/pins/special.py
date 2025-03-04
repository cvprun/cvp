# -*- coding: utf-8 -*-

from typing import (
    Annotated,
    Any,
    Final,
    Optional,
    Sequence,
    Union,
    get_args,
    get_origin,
)

from cvp.dtypes.dtype import Dtype
from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.pins.annotated import get_arcs, get_docs, get_name
from cvp.pins.datas import DataOutputPinTemplate
from cvp.pins.flows import FlowInputPinTemplate, FlowOutputPinTemplate
from cvp.pins.kind import PinKind


class EntrypointPin(FlowInputPinTemplate):
    def __init__(
        self,
        name: Optional[str] = None,
        docs: Optional[str] = None,
        arcs: Optional[Sequence[str]] = None,
    ):
        super().__init__(
            name=name if name else "entrypoint",
            docs=docs if docs else "Indicates the starting point of the flow",
            arcs=arcs,
        )


class PrevPin(FlowInputPinTemplate):
    def __init__(
        self,
        name: Optional[str] = None,
        docs: Optional[str] = None,
        arcs: Optional[Sequence[str]] = None,
    ):
        super().__init__(
            name=name if name else "prev",
            docs=docs if docs else "Marks the starting point of a generic function",
            arcs=arcs,
        )


class NextPin(FlowOutputPinTemplate):
    def __init__(
        self,
        name: Optional[str] = None,
        docs: Optional[str] = None,
        arcs: Optional[Sequence[str]] = None,
    ):
        super().__init__(
            name=name if name else "next",
            docs=docs if docs else "Marks the endpoint of a generic function",
            arcs=arcs,
        )


DEFAULT_RETURN_PIN_NAME: Final[str] = "return"
DEFAULT_RETURN_PIN_DOCS: Final[str] = "The return value of a function"


class ReturnPin(DataOutputPinTemplate):
    def __init__(
        self,
        dtype: Dtype,
        docs: Optional[str] = None,
        arcs: Optional[Sequence[str]] = None,
        *,
        name: Optional[str] = None,
    ):
        super().__init__(
            name=name if name else DEFAULT_RETURN_PIN_NAME,
            dtype=dtype,
            docs=docs if docs else DEFAULT_RETURN_PIN_DOCS,
            arcs=arcs,
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
            return_name = get_name(*return_args, default=DEFAULT_RETURN_PIN_NAME)
            return_docs = get_docs(*return_args, default=DEFAULT_RETURN_PIN_DOCS)
            return_arcs = get_arcs(*return_args)
        else:
            return_dtype = dtype_registry.get(return_annotation)
            return_name = DEFAULT_RETURN_PIN_NAME
            return_docs = DEFAULT_RETURN_PIN_DOCS
            return_arcs = list()

        return cls(
            dtype=return_dtype,
            docs=return_docs,
            arcs=return_arcs,
            name=return_name,
        )
