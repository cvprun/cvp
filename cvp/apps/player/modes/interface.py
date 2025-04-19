# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Sequence

from pygame import Event
from pygame.key import ScancodeWrapper

from cvp.msgs.msg import Msg


class ModeInterface(ABC):
    @classmethod
    @abstractmethod
    def get_mode_name(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_mode_menus(cls) -> Sequence[str]:
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
