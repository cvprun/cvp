# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.config.sections.appearance import AppMode
from cvp.msgs.msg import Msg
from cvp.renderer.context import RendererContext
from cvp.types.override import override


class ModeInterface(ABC):
    @staticmethod
    @abstractmethod
    def get_mode() -> AppMode:
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
    def do_process(self) -> None:
        raise NotImplementedError


class BaseMode(ModeInterface, ABC):
    def __init__(self, context: RendererContext):
        self._context = context

    @property
    def context(self) -> RendererContext:
        return self._context

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
