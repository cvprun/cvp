# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional, Protocol, runtime_checkable

from cvp.apps.player.windows.canvas import CanvasWindow
from cvp.context.context import Context
from cvp.types.override import override


@runtime_checkable
class CanvasWindowNameProtocol(Protocol):
    __cvp_canvas_window_name__: str


class CanvasWindowInterface(ABC):
    @abstractmethod
    def get_window_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def do_process(self, window: Optional[CanvasWindow]) -> None:
        raise NotImplementedError


class BaseCanvasWindow(CanvasWindowInterface, CanvasWindowNameProtocol, ABC):
    def __init__(self, context: Context):
        assert isinstance(self, CanvasWindowNameProtocol)
        self._context = context

    @override
    def get_window_name(self) -> str:
        return self.__cvp_canvas_window_name__

    @property
    def context(self) -> Context:
        return self._context
