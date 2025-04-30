# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

from cvp.context.context import Context
from cvp.onvif.config import OnvifConfig
from cvp.types.override import override


@runtime_checkable
class OnvifTabNameProtocol(Protocol):
    __cvp_onvif_tab_name__: str


class OnvifTabInterface(ABC):
    @classmethod
    @abstractmethod
    def get_tab_name(cls) -> str:
        raise NotImplementedError

    @abstractmethod
    def do_process(self, onvif: OnvifConfig) -> None:
        raise NotImplementedError


class BaseOnvifTab(OnvifTabInterface, OnvifTabNameProtocol, ABC):
    def __init__(self, context: Context):
        assert isinstance(self, OnvifTabNameProtocol)
        self._context = context

    @classmethod
    @override
    def get_tab_name(cls) -> str:
        return cls.__cvp_onvif_tab_name__

    @property
    def context(self) -> Context:
        return self._context

    @property
    def onvifs(self):
        return self._context.onvifs
