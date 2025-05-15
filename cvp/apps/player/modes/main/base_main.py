# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from types import ModuleType
from typing import Any, Iterable, Optional, Set, Type

from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.main.interface import WindowInterface
from cvp.apps.player.modes.main.layout import MainLayout
from cvp.imgui.menu_container import MenuItemLike, MenuList
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.interface import PopupInterface
from cvp.msgs.msg import Msg
from cvp.types.override import override


class BaseMainModeInterface(ABC):
    @abstractmethod
    def get_selected_main_key(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_main_key_set(self) -> Set[str]:
        raise NotImplementedError

    @abstractmethod
    def on_window_popped(self, window: WindowInterface) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_window_creation(self, key: str) -> WindowInterface:
        raise NotImplementedError


class BaseMainMode(BaseMode, BaseMainModeInterface, ABC):
    def __init__(
        self,
        layout: MainLayout,
        module: ModuleType,
        main_window_type: Type[WindowInterface],
        *,
        menus: Optional[Iterable[MenuItemLike]] = None,
        popups: Optional[Iterable[PopupInterface[Any]]] = None,
    ):
        super().__init__(layout.context)
        self._layout = layout
        self._module = module
        self._main_window_type = main_window_type
        self._menus = MenuList.from_iterable(menus or ())
        self._popups = PopupList.from_iterable(popups or ())

    @property
    def initialized(self) -> bool:
        return self._layout.initialized

    def filter_window_key_set(self) -> Set[str]:
        return self._layout.filter_window_key_set(self._main_window_type)

    def do_sync_main_windows(self) -> None:
        main_keys = self.get_main_key_set()
        window_keys = self.filter_window_key_set()
        if main_keys == window_keys:
            return

        remove_keys = window_keys - main_keys
        create_keys = main_keys - window_keys

        for key in remove_keys:
            self.on_window_popped(self._layout.mains.pop(key))

        for key in create_keys:
            self._layout.add_main_window(key, self.on_window_creation(key))

        assert self.get_main_key_set() == self.filter_window_key_set()

    @property
    def selected_main_window(self):
        return self._layout.get_main_window(self.get_selected_main_key())

    @override
    def on_main_menu(self) -> None:
        self._menus.do_process()

        if window := self.selected_main_window:
            window.on_main_menu()

        self._layout.do_window_menu("Window", self._module)

    @override
    def on_status_menu(self) -> None:
        if window := self.selected_main_window:
            window.on_status_menu()

    @override
    def on_event(self, event: Event) -> bool:
        if window := self.selected_main_window:
            return window.on_event(event)
        else:
            return False

    @override
    def on_msg(self, msg: Msg) -> bool:
        if window := self.selected_main_window:
            return window.on_msg(msg)
        else:
            return False

    @override
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        if window := self.selected_main_window:
            window.on_keyboard(keys)

    @override
    def on_process(self) -> None:
        self._layout.do_dockspace_process()
        self.do_sync_main_windows()
        self._layout.do_process(self._module)
        self._popups.do_process()
