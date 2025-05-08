# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Sequence


class InputHandlerInterface(ABC):
    @abstractmethod
    def get_method_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_keyboard_layout(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_language(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def has_composing(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_composing(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def del_composing(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def clear_composing(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def add(self, text: str) -> Sequence[str]:
        raise NotImplementedError
