# -*- coding: utf-8 -*-

from inspect import Parameter
from typing import Annotated, Any, Optional, Sequence, Union, get_args, get_origin

from cvp.dtypes.dtype import Dtype
from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.inspect.parameter import inspect_parameter_required
from cvp.pins.action import Action
from cvp.pins.annotated import (
    get_action,
    get_arcs,
    get_default,
    get_docs,
    get_name,
    get_required,
    get_stream,
)
from cvp.pins.kind import PinKind, parameter_to_kind
from cvp.pins.markers import NoDefault
from cvp.pins.stream import Stream


class Pin:
    def __init__(
        self,
        name: str,
        dtype: Optional[Dtype] = None,
        docs: Optional[str] = None,
        action: Optional[Action] = None,
        stream: Optional[Stream] = None,
        required: Optional[bool] = None,
        arcs: Optional[Sequence[str]] = None,
        kind: Optional[PinKind] = None,
        default: Any = NoDefault,
    ):
        self.name = name
        self.dtype = dtype
        self.docs = docs if docs else str()
        self.action = action if action is not None else Action.data
        self.stream = stream if stream is not None else Stream.input
        self.required = bool(required)
        self.arcs = list(arcs if arcs else [])
        self.kind = kind if kind is not None else PinKind.unknown
        self.default = default

    @classmethod
    def from_parameter(
        cls,
        parameter: Parameter,
        *,
        dtype_registry: Optional[DtypeRegistry] = None,
    ):
        if dtype_registry is None:
            dtype_registry = global_dtype_registry()
        assert dtype_registry is not None

        param_origin = get_origin(parameter.annotation)
        if param_origin == Union:
            raise TypeError("Union parameter is not supported")

        param_required = inspect_parameter_required(parameter)
        param_kind = parameter_to_kind(parameter)

        if param_origin == Annotated:
            param_args = get_args(parameter.annotation)
            assert 2 <= len(param_args)
            param_dtype = dtype_registry.get(param_args[0])
            param_name = get_name(*param_args, default=parameter.name)
            param_docs = get_docs(*param_args, default=None)
            param_action = get_action(*param_args, default=Action.data)
            param_stream = get_stream(*param_args, default=Stream.input)
            param_arcs = get_arcs(*param_args)
            param_default = get_default(*param_args, default=parameter.default)
            param_required = get_required(*param_args, default=param_required)
        else:
            param_dtype = dtype_registry.get(parameter.annotation)
            param_name = parameter.name
            param_docs = str()
            param_action = Action.data
            param_stream = Stream.input
            param_arcs = list()
            param_default = parameter.default

        return cls(
            name=param_name,
            dtype=param_dtype,
            docs=param_docs,
            action=param_action,
            stream=param_stream,
            required=param_required,
            arcs=param_arcs,
            kind=param_kind,
            default=param_default,
        )

    @property
    def has_dtype(self):
        return self.dtype is not None

    @property
    def path(self):
        return self.dtype.path if self.dtype else str()

    @property
    def is_data_action(self):
        return self.action == Action.data

    @property
    def is_flow_action(self):
        return self.action == Action.flow

    @property
    def is_input_stream(self):
        return self.stream == Stream.input

    @property
    def is_output_stream(self):
        return self.stream == Stream.output

    @property
    def is_flow_inputs(self) -> bool:
        return self.is_flow_action and self.is_input_stream

    @property
    def is_flow_outputs(self) -> bool:
        return self.is_flow_action and self.is_output_stream

    @property
    def is_data_inputs(self) -> bool:
        return self.is_data_action and self.is_input_stream

    @property
    def is_data_outputs(self) -> bool:
        return self.is_data_action and self.is_output_stream

    @property
    def has_default(self) -> bool:
        return self.default != NoDefault
