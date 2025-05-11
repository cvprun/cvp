# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from types import ModuleType
from typing import Any, Callable, Iterable, Optional, Set, Tuple, Type

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.main.interface import WindowInterface
from cvp.apps.player.modes.main.layout import MainLayout
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.interface import PopupInterface
from cvp.msgs.msg import Msg
from cvp.types.override import override


class BaseMainModeInterface(ABC):
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
        menus: Optional[Iterable[Tuple[str, Callable[[], None]]]] = None,
        popups: Optional[Iterable[PopupInterface[Any]]] = None,
    ):
        super().__init__(layout.context)
        self._layout = layout
        self._module = module
        self._main_window_type = main_window_type
        self._menus = list(menus or ())
        self._popups = PopupList(popups or ())

    @property
    def initialized(self) -> bool:
        return self._layout.initialized

    @property
    def focused_key(self) -> str:
        return self._layout.focused_key

    @focused_key.setter
    def focused_key(self, value: str) -> None:
        self._layout.focused_key = value

    @property
    def focused_window(self):
        return self._layout.focused_window

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

    @override
    def on_main_menu(self) -> None:
        for name, func in self._menus:
            if imgui.begin_menu(name):
                try:
                    func()
                finally:
                    imgui.end_menu()

        self._layout.do_main_menu()
        self._layout.do_window_menu("Window", self._module)

    @override
    def on_status_menu(self) -> None:
        self._layout.do_status_menu()

    @override
    def on_event(self, event: Event) -> bool:
        return self._layout.do_event(event)

    @override
    def on_msg(self, msg: Msg) -> bool:
        return self._layout.do_msg(msg)

    @override
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        self._layout.do_keyboard(keys)

    @override
    def on_process(self) -> None:
        self._layout.do_dockspace_process()
        self.do_sync_main_windows()
        self._layout.do_process(self._module)
        self._popups.do_process()
