# -*- coding: utf-8 -*-

from copy import deepcopy
from inspect import Parameter
from typing import (
    Annotated,
    Any,
    Iterable,
    NewType,
    Optional,
    Sequence,
    Union,
    get_args,
    get_origin,
)

from cvp.dtypes.dtype import Dtype
from cvp.inspect.parameter import NoDefault, inspect_parameter_required
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
from cvp.variables import NODOC

PinName = NewType("PinName", str)
WireKey = NewType("WireKey", str)


class Pin:
    def __init__(
        self,
        name: PinName,
        dtype: Union[None, type, Dtype],
        action: Action,
        stream: Stream,
        kind: PinKind,
        default=NoDefault,
        docs=NODOC,
        wires: Optional[Iterable[WireKey]] = None,
        *,
        required=False,
        hidden=False,
    ):
        if not name:
            raise ValueError("The 'name' argument is required")

        self.__dtype = dtype if isinstance(dtype, Dtype) else Dtype(dtype)
        self.__name = name
        self.__action = action
        self.__stream = stream
        self.__kind = kind

        self.__default = default
        self.__docs = docs
        self.__wires = tuple(wires if wires else ())

        self.__required = required
        self.__hidden = hidden

    @classmethod
    def from_parameter(cls, parameter: Parameter):
        param_origin = get_origin(parameter.annotation)
        if param_origin == Union:
            raise TypeError("Union parameter is not supported")

        param_kind = parameter_to_kind(parameter)
        param_required = inspect_parameter_required(parameter)

        if param_origin == Annotated:
            param_args = get_args(parameter.annotation)
            assert 2 <= len(param_args)

            param_type = param_args[0]
            if not isinstance(param_type, type):
                raise TypeError("Parameters only accept instances of types")

            param_dtype = Dtype(param_type)  # type: ignore[var-annotated]

            annotated_args = param_args[1:]
            param_name = PinName(get_name(*annotated_args, default=parameter.name))
            param_action = get_action(*annotated_args, default=Action.data)
            param_stream = get_stream(*annotated_args, default=Stream.input)
            param_default = get_default(*annotated_args, default=parameter.default)
            param_docs = get_docs(*annotated_args, default=None)
            param_wires = list(WireKey(w) for w in get_wires(*annotated_args))
            param_required = get_required(*annotated_args, default=param_required)
            param_hidden = get_hidden(*annotated_args, default=False)
        else:
            param_dtype = Dtype(parameter.annotation)
            param_name = PinName(parameter.name)
            param_action = Action.data
            param_stream = Stream.input
            param_default = parameter.default
            param_docs = str()
            param_wires = list()
            param_hidden = False

        return cls(
            name=param_name,
            dtype=param_dtype,
            action=param_action,
            stream=param_stream,
            kind=param_kind,
            default=param_default,
            docs=param_docs,
            wires=param_wires,
            required=param_required,
            hidden=param_hidden,
        )

    @property
    def name(self) -> PinName:
        return self.__name

    @property
    def dtype(self) -> Dtype:
        return self.__dtype

    @property
    def action(self) -> Action:
        return self.__action

    @property
    def stream(self) -> Stream:
        return self.__stream

    @property
    def kind(self) -> PinKind:
        return self.__kind

    @property
    def required(self) -> bool:
        return self.__required

    @property
    def hidden(self) -> bool:
        return self.__hidden

    @property
    def default(self) -> Any:
        return self.__default

    @property
    def has_default(self) -> bool:
        return self.__default is not NoDefault

    def deepcopy_default(self):
        return deepcopy(self.default) if self.has_default else None

    @property
    def docs(self) -> str:
        return self.__docs

    @property
    def wires(self) -> Sequence[WireKey]:
        return self.__wires

    @property
    def type(self):
        return self.__dtype.type

    @property
    def path(self):
        return self.__dtype.path

    @property
    def type_docs(self):
        return self.__dtype.docs

    @property
    def module_path(self) -> str:
        return self.__dtype.module_path

    @property
    def class_name(self) -> str:
        return self.__dtype.class_name

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
