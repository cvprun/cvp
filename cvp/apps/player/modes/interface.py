# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any

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
    def get_mode_number(cls) -> int:
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


def retrieve_mode_instances(o: Any):
    result = list()
    for key in dir(o):
        if value := getattr(o, key, None):
            if isinstance(value, ModeInterface):
                result.append(value)
    return result
