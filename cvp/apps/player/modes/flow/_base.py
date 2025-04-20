# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

from cvp.context.context import Context
from cvp.types.override import override


@runtime_checkable
class FlowWindowNameProtocol(Protocol):
    __cvp_flow_window_name__: str


class FlowWindowInterface(ABC):
    @classmethod
    @abstractmethod
    def get_window_name(cls) -> str:
        raise NotImplementedError

    @abstractmethod
    def do_process(self) -> None:
        raise NotImplementedError


class BaseFlowWindow(FlowWindowInterface, FlowWindowNameProtocol, ABC):
    def __init__(self, context: Context):
        assert isinstance(self, FlowWindowNameProtocol)
        self._context = context

    @classmethod
    @override
    def get_window_name(cls) -> str:
        return cls.__cvp_flow_window_name__

    @property
    def context(self) -> Context:
        return self._context

    @property
    def flows(self):
        return self._context.flows
