# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from sys import exc_info
from typing import Any, Callable, List, Optional, Sequence

from cvp.flow.record import FlowRecord
from cvp.flow.templates.pin import PinTemplate
from cvp.flow.templates.pin.special import NextPinTemplate, PrevPinTemplate
from cvp.types.colors import RGBA, WHITE_RGBA
from cvp.types.override import override


class NodeTemplateInterface(ABC):
    @abstractmethod
    def run(self, pin: PinTemplate, context: FlowRecord) -> Optional[PinTemplate]:
        raise NotImplementedError


class NodeTemplate(NodeTemplateInterface):
    def __init__(
        self,
        name: str,
        path: str,
        func: Optional[Callable] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
        pins: Optional[Sequence[PinTemplate]] = None,
        tags: Optional[Sequence[str]] = None,
    ):
        self.name = name
        self.path = path
        self.func = func
        self.docs = docs if docs else str()
        self.icon = icon if icon else str()
        self.color = color if color else WHITE_RGBA
        self.pins = list(pins if pins else [])
        self.tags = list(tags if tags else [])

    @property
    def flow_inputs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_flow_inputs, self.pins))

    @property
    def flow_outputs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_flow_outputs, self.pins))

    @property
    def data_inputs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_data_inputs, self.pins))

    @property
    def data_outputs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_data_outputs, self.pins))

    @property
    def is_bypass_flow(self) -> bool:
        if len(self.pins) != 2:
            return False

        flow_inputs = self.flow_inputs
        if len(flow_inputs) != 1:
            return False

        flow_outputs = self.flow_outputs
        if len(flow_outputs) != 1:
            return False

        if not isinstance(flow_inputs[0], PrevPinTemplate):
            return False
        if not isinstance(flow_outputs[0], NextPinTemplate):
            return False

        assert 0 == len(self.data_inputs)
        assert 0 == len(self.data_outputs)
        return True

    def __call__(self, *args, **kwargs) -> Any:
        if self.func is None:
            raise ValueError("Node function is not set")
        return self.func(*args, **kwargs)

    @override
    def run(self, pin: PinTemplate, context: FlowRecord) -> Optional[PinTemplate]:
        try:
            context.set_result(self.__call__(*context.args, **context.kwargs))
        except:  # noqa
            context.set_exception(exc_info())

        if self.is_bypass_flow:
            return self.flow_outputs[0]
        else:
            return None
