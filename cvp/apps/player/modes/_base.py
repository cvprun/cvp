# -*- coding: utf-8 -*-

from typing import Protocol, Sequence, runtime_checkable

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
    def get_mode_menus(cls) -> Sequence[str]:
        return ()

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

    @override
    def do_process(self) -> None:
        pass

    def get_selected_submenu(self, *, suffix=None) -> str:
        return self._context.get_selected_submenu(type(self), suffix=suffix)

    def set_selected_submenu(self, value: str, *, suffix=None) -> None:
        self._context.set_selected_submenu(type(self), value, suffix=suffix)

    @property
    def selected(self) -> str:
        return self.get_selected_submenu()

    @selected.setter
    def selected(self, value: str) -> None:
        self.set_selected_submenu(value)

    def begin_mode_context(self):
        return begin_mode_context(type(self).__name__)
