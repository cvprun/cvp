# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

PopupResultT = TypeVar("PopupResultT")


class PopupInterface(Generic[PopupResultT], ABC):
    @abstractmethod
    def is_opened(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_min_width(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_min_height(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def on_process(self) -> Optional[PopupResultT]:
        raise NotImplementedError
