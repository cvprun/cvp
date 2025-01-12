# -*- coding: utf-8 -*-

from inspect import Parameter
from typing import Any, List, Optional

from cvp.flow.datas.action import Action
from cvp.flow.datas.stream import Stream


class PinTemplate:
    def __init__(
        self,
        name: str,
        dtype: Optional[str] = None,
        docs: Optional[str] = None,
        action: Optional[Action] = None,
        stream: Optional[Stream] = None,
        required: Optional[bool] = None,
        arcs: Optional[List[str]] = None,
        default: Any = Parameter.empty,
    ):
        self.name = name
        self.docs = docs if docs else str()
        self.dtype = dtype if dtype else str()
        self.action = action if action is not None else Action.data
        self.stream = stream if stream is not None else Stream.input
        self.required = bool(required)
        self.arcs = list(arcs if arcs else [])
        self.default = default

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
