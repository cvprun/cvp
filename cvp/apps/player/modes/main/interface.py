# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any

from pygame import Event
from pygame.key import ScancodeWrapper

from cvp.msgs.msg import Msg


class WindowInterface(ABC):
    @abstractmethod
    def get_window_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def on_main_menu(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_status_menu(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_event(self, event: Event) -> bool:
        raise NotImplementedError

    @abstractmethod
    def on_msg(self, msg: Msg) -> bool:
        raise NotImplementedError

    @abstractmethod
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        raise NotImplementedError

    @abstractmethod
    def do_process(self) -> None:
        raise NotImplementedError


def retrieve_window_instances(o: Any):
    result = list()
    for key in dir(o):
        if value := getattr(o, key, None):
            if isinstance(value, WindowInterface):
                result.append(value)
    return result
