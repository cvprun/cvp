# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional, Protocol, runtime_checkable

from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.windows.graph import FlowGraphWindow
from cvp.context.context import Context
from cvp.msgs.msg import Msg
from cvp.types.override import override


@runtime_checkable
class FlowWindowNameProtocol(Protocol):
    __cvp_flow_window_name__: str


class FlowWindowInterface(ABC):
    @abstractmethod
    def get_window_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def on_main_menu(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def do_event(self, event: Event) -> bool:
        raise NotImplementedError

    @abstractmethod
    def do_msg(self, msg: Msg) -> bool:
        raise NotImplementedError

    @abstractmethod
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        raise NotImplementedError

    @abstractmethod
    def do_process(self, window: Optional[FlowGraphWindow]) -> None:
        raise NotImplementedError


class BaseFlowWindow(FlowWindowInterface, FlowWindowNameProtocol, ABC):
    def __init__(self, context: Context):
        assert isinstance(self, FlowWindowNameProtocol)
        self._context = context

    @override
    def get_window_name(self) -> str:
        return self.__cvp_flow_window_name__

    @override
    def on_main_menu(self) -> None:
        pass

    @override
    def do_event(self, event: Event) -> bool:
        return False

    @override
    def do_msg(self, msg: Msg) -> bool:
        return False

    @override
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        pass

    @property
    def context(self) -> Context:
        return self._context
