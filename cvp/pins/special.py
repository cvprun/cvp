# -*- coding: utf-8 -*-

from typing import Annotated, Any, Optional, Sequence, Union, get_args, get_origin

from cvp.dtypes.dtype import Dtype
from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.pins.annotated import get_arcs, get_docs, get_name
from cvp.pins.datas import DataOutputPin
from cvp.pins.flows import FlowInputPin, FlowOutputPin


class EntrypointPin(FlowInputPin):
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


class PrevPin(FlowInputPin):
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


class NextPin(FlowOutputPin):
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


class ReturnPin(DataOutputPin):
    def __init__(
        self,
        name: Optional[str] = None,
        docs: Optional[str] = None,
        dtype: Optional[Dtype] = None,
        arcs: Optional[Sequence[str]] = None,
    ):
        super().__init__(
            name=name if name else "return",
            dtype=dtype,
            docs=docs if docs else "The return value of a function",
            arcs=arcs,
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

        default_return_pin = cls()
        default_name = default_return_pin.name
        default_docs = default_return_pin.docs

        if return_origin == Annotated:
            return_args = get_args(return_annotation)
            assert 2 <= len(return_args)
            return_dtype = dtype_registry.get(return_args[0])
            return_name = get_name(*return_args, default=default_name)
            return_docs = get_docs(*return_args, default=default_docs)
            return_arcs = get_arcs(*return_args)
        else:
            return_dtype = dtype_registry.get(return_annotation)
            return_name = default_name
            return_docs = default_docs
            return_arcs = list()

        return cls(
            name=return_name,
            docs=return_docs,
            dtype=return_dtype,
            arcs=return_arcs,
        )
