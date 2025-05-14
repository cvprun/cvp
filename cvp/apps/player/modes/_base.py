# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Protocol, runtime_checkable

from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes.interface import ModeInterface
from cvp.context.context import Context
from cvp.imgui.begin_mode import begin_mode_context
from cvp.msgs.msg import Msg
from cvp.types.override import override


@runtime_checkable
class BaseModeProtocol(Protocol):
    __cvp_mode_name__: str
    __cvp_mode_icon__: str


class BaseMode(ModeInterface, BaseModeProtocol):
    def __init__(self, context: Context):
        assert isinstance(self, BaseModeProtocol)
        self._context = context

    @property
    def context(self) -> Context:
        return self._context

    @classmethod
    @override
    def get_mode_name(cls) -> str:
        return cls.__cvp_mode_name__

    @classmethod
    @override
    def get_mode_icon(cls) -> str:
        return cls.__cvp_mode_icon__

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

    @override
    def on_process(self) -> None:
        pass

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

    def get_recent_items(self, *, suffix=None):
        return self._context.get_recent_items(type(self), suffix=suffix)

    def add_recent_item(
        self,
        value: str,
        accessed_at: Optional[datetime] = None,
        *,
        suffix=None,
    ) -> None:
        self._context.add_recent_item(
            type(self),
            value,
            accessed_at,
            suffix=suffix,
        )

    def clear_recent_items(self, *, suffix=None) -> None:
        self._context.clear_recent_items(type(self), suffix=suffix)

    def begin_mode_context(self):
        return begin_mode_context(type(self).__name__)
