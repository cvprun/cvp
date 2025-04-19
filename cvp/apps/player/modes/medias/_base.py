# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

from cvp.context.context import Context
from cvp.media.config import MediaConfig
from cvp.types.override import override


@runtime_checkable
class MediaTabNameProtocol(Protocol):
    __cvp_media_tab_name__: str


class MediaTabInterface(ABC):
    @classmethod
    @abstractmethod
    def get_tab_name(cls) -> str:
        raise NotImplementedError

    @abstractmethod
    def do_process(self, media: MediaConfig) -> None:
        raise NotImplementedError


class BaseMediaTab(MediaTabInterface, MediaTabNameProtocol, ABC):
    def __init__(self, context: Context):
        assert isinstance(self, MediaTabNameProtocol)
        self._context = context

    @classmethod
    @override
    def get_tab_name(cls) -> str:
        return cls.__cvp_media_tab_name__

    @property
    def context(self) -> Context:
        return self._context

    @property
    def medias(self):
        return self._context.medias
