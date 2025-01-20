# -*- coding: utf-8 -*-

from inspect import Parameter
from typing import Any, Optional, Sequence

from cvp.dtypes.dtype import Dtype
from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.pins.action import Action
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
        default: Any = NoDefault,
    ):
        self.name = name
        self.dtype = dtype
        self.docs = docs if docs else str()
        self.action = action if action is not None else Action.data
        self.stream = stream if stream is not None else Stream.input
        self.required = bool(required)
        self.arcs = list(arcs if arcs else [])
        self.default = default

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

    @staticmethod
    def inspect_parameter_required(parameter: Parameter) -> bool:
        match parameter.kind:
            case Parameter.POSITIONAL_ONLY:
                return parameter.default == Parameter.empty
            case Parameter.POSITIONAL_OR_KEYWORD:
                return parameter.default == Parameter.empty
            case Parameter.VAR_POSITIONAL:
                return False
            case Parameter.KEYWORD_ONLY:
                return parameter.default == Parameter.empty
            case Parameter.VAR_KEYWORD:
                return False
            case _:
                raise ValueError(f"Unexpected parameter kind: {parameter.kind}")

    @classmethod
    def from_parameter(
        cls,
        parameter: Parameter,
        docs: Optional[str] = None,
        arcs: Optional[Sequence[str]] = None,
        *,
        dtype_registry: Optional[DtypeRegistry] = None,
    ):
        if dtype_registry is None:
            dtype_registry = global_dtype_registry()

        assert dtype_registry is not None
        dtype = dtype_registry.get(parameter.annotation)
        required = cls.inspect_parameter_required(parameter)

        return cls(
            name=parameter.name,
            dtype=dtype,
            docs=docs if docs else str(),
            action=Action.data,
            stream=Stream.input,
            required=required,
            arcs=arcs,
            default=parameter.default,
        )
