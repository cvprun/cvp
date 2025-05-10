# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional, Protocol, Union, runtime_checkable

from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes.main.interface import WindowInterface
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.flags.window import WindowFlags
from cvp.msgs.msg import Msg
from cvp.types.override import override


@runtime_checkable
class WindowNameProtocol(Protocol):
    __cvp_window_name__: str


class BaseWindowInterface(ABC):
    @abstractmethod
    def get_window_flags(self) -> Union[WindowFlags, int]:
        raise NotImplementedError

    @abstractmethod
    def do_main_process(self) -> None:
        raise NotImplementedError


class BaseWindow(WindowInterface, BaseWindowInterface, WindowNameProtocol):
    def __init__(self, context: Context):
        assert isinstance(self, WindowNameProtocol)
        self._context = context

    @override
    def get_window_name(self) -> str:
        return self.__cvp_window_name__

    @override
    def get_opened_window(self) -> Optional[bool]:
        return self._context.get_opened_window(type(self))

    @override
    def set_opened_window(self, value: bool) -> None:
        self._context.set_opened_window(type(self), value)

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

    @focused_key.setter
    def focused_key(self, value: str) -> None:
        self._context.config.navigation.focused_key = value

    @property
    def opened_window(self) -> bool:
        return bool(self.get_opened_window())

    @opened_window.setter
    def opened_window(self, value: bool) -> None:
        self.set_opened_window(value)

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

    @override
    def do_process(self) -> None:
        opened = self.opened_window
        if not opened:
            return

        with begin_context(
            self.get_window_name(),
            closable=opened,
            flags=self.get_window_flags(),
        ) as result:
            assert result.value is not None
            if opened != result.value:
                self.opened_window = result.value

            if not result.value:
                return

            if not result.opened:
                return

            self.do_main_process()

    @override
    def get_window_flags(self) -> Union[WindowFlags, int]:
        return 0

    @override
    def do_main_process(self) -> None:
        pass
