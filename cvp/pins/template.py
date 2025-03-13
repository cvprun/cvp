# -*- coding: utf-8 -*-

from inspect import Parameter
from typing import (
    Annotated,
    Iterable,
    NewType,
    Optional,
    Union,
    get_args,
    get_origin,
)

from cvp.dtypes.dtype import Dtype
from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.inspect.parameter import NoDefault, inspect_parameter_required
from cvp.modules.class_path import ClassPath
from cvp.pins.action import Action
from cvp.pins.annotated import (
    get_action,
    get_default,
    get_docs,
    get_hidden,
    get_name,
    get_required,
    get_stream,
    get_wires,
)
from cvp.pins.kind import PinKind, parameter_to_kind
from cvp.pins.stream import Stream

PinName = NewType("PinName", str)
WireKey = NewType("WireKey", str)


class PinTemplate:
    def __init__(
        self,
        name: PinName,
        dtype: Union[None, Dtype, ClassPath, type],
        action: Action,
        stream: Stream,
        docs: Optional[str] = None,
        required=False,
        hidden=False,
        wires: Optional[Iterable[WireKey]] = None,
        kind=PinKind.unknown,
        default=NoDefault,
    ):
        if not name:
            raise ValueError("The 'name' argument is required")

        if dtype is None:
            self._dtype = Dtype(type(None))
        elif isinstance(dtype, Dtype):
            self._dtype = dtype
        elif isinstance(dtype, ClassPath):
            self._dtype = Dtype(dtype)
        elif isinstance(dtype, type):
            self._dtype = Dtype(dtype)
        else:
            raise TypeError(f"Unsupported dtype type: {type(dtype).__name__}")

        self._name = name
        self._action = action
        self._stream = stream

        self.docs = docs if docs else str()
        self.required = bool(required)
        self.hidden = bool(hidden)
        self.wires = list(wires if wires else ())
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
            param_name = PinName(get_name(*param_args, default=parameter.name))
            param_action = get_action(*param_args, default=Action.data)
            param_stream = get_stream(*param_args, default=Stream.input)
            param_docs = get_docs(*param_args, default=None)
            param_wires = list(WireKey(w) for w in get_wires(*param_args))
            param_default = get_default(*param_args, default=parameter.default)
            param_required = get_required(*param_args, default=param_required)
            param_hidden = get_hidden(*param_args, default=False)
        else:
            param_dtype = dtype_registry.get(parameter.annotation)
            param_name = PinName(parameter.name)
            param_action = Action.data
            param_stream = Stream.input
            param_docs = str()
            param_wires = list()
            param_default = parameter.default
            param_hidden = False

        return cls(
            name=param_name,
            dtype=param_dtype,
            action=param_action,
            stream=param_stream,
            docs=param_docs,
            required=param_required,
            hidden=param_hidden,
            wires=param_wires,
            kind=param_kind,
            default=param_default,
        )

    @property
    def name(self) -> PinName:
        return self._name

    @property
    def dtype(self) -> Dtype:
        return self._dtype

    @property
    def action(self) -> Action:
        return self._action

    @property
    def stream(self) -> Stream:
        return self._stream

    @property
    def path(self):
        return self._dtype.path

    @property
    def module_path(self) -> str:
        return self._dtype.module_path

    @property
    def class_name(self) -> str:
        return self._dtype.class_name

    @property
    def is_data_action(self):
        return self.action == Action.data

    @property
    def is_exec_action(self):
        return self.action == Action.exec

    @property
    def is_input_stream(self):
        return self.stream == Stream.input

    @property
    def is_output_stream(self):
        return self.stream == Stream.output

    @property
    def is_exec_inputs(self) -> bool:
        return self.is_exec_action and self.is_input_stream

    @property
    def is_exec_outputs(self) -> bool:
        return self.is_exec_action and self.is_output_stream

    @property
    def is_data_inputs(self) -> bool:
        return self.is_data_action and self.is_input_stream

    @property
    def is_data_outputs(self) -> bool:
        return self.is_data_action and self.is_output_stream

    @property
    def has_default(self) -> bool:
        return self.default != NoDefault
