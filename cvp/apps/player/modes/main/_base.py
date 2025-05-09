# -*- coding: utf-8 -*-

from abc import ABC
from typing import Protocol, runtime_checkable

from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes.main.interface import WindowInterface
from cvp.context.context import Context
from cvp.msgs.msg import Msg
from cvp.types.override import override


@runtime_checkable
class WindowNameProtocol(Protocol):
    __cvp_window_name__: str


class BaseWindow(WindowInterface, WindowNameProtocol, ABC):
    def __init__(self, context: Context):
        assert isinstance(self, WindowNameProtocol)
        self._context = context

    @override
    def get_window_name(self) -> str:
        return self.__cvp_window_name__

    @override
    def on_main_menu(self) -> None:
        pass

    @override
    def on_status_menu(self) -> None:
        pass

    @override
    def on_event(self, event: Event) -> bool:
        return False

    @override
    def on_msg(self, msg: Msg) -> bool:
        return False

    @override
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        pass

    @property
    def context(self) -> Context:
        return self._context

    @property
    def focused_key(self) -> str:
        return self._context.config.navigation.focused_key

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
