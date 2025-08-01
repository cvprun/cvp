# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class LinesInterface(ABC):
    @abstractmethod
    def getvalue(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def write(self, text: str) -> None:
        raise NotImplementedError
