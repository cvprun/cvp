# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Protocol, runtime_checkable

from cvp.context.context import Context
from cvp.types.override import override


@runtime_checkable
class FlowWindowNameProtocol(Protocol):
    __cvp_flow_window_name__: str


class FlowWindowInterface(ABC):
    @abstractmethod
    def get_window_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def do_process(self) -> None:
        raise NotImplementedError


class BaseFlowWindow(FlowWindowInterface, FlowWindowNameProtocol, ABC):
    def __init__(self, context: Context):
        assert isinstance(self, FlowWindowNameProtocol)
        self._context = context

    @override
    def get_window_name(self) -> str:
        return self.__cvp_flow_window_name__

    @property
    def context(self) -> Context:
        return self._context

    @property
    def flows(self):
        return self._context.flows

    def get_selected_submenu(self, *, suffix=None) -> str:
        return self._context.get_selected_submenu(type(self), suffix=suffix)

    def set_selected_submenu(self, value: str, *, suffix=None) -> None:
        self._context.set_selected_submenu(type(self), value, suffix=suffix)

    @property
    def selected_submenu(self) -> str:
        return self.get_selected_submenu()

    @selected_submenu.setter
    def selected_submenu(self, value: str) -> None:
        self.set_selected_submenu(value)

    def get_recent_items(self, *, suffix=None) -> str:
        return self._context.get_recent_items(type(self), suffix=suffix)

    @property
    def recent_items(self) -> str:
        return self.get_recent_items()

    def add_recent_item(
        self,
        value: str,
        accessed_at: Optional[datetime] = None,
        *,
        suffix=None,
    ) -> None:
        self._context.add_recent_item(type(self), value, accessed_at, suffix=suffix)
