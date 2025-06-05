# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ValueT = TypeVar("ValueT")


class ProxyValue(Generic[ValueT], ABC):
    @abstractmethod
    def get(self) -> ValueT:
        raise NotImplementedError

    @abstractmethod
    def set(self, value: ValueT) -> None:
        raise NotImplementedError
