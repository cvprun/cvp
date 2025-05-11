# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

from cvp.context.context import Context
from cvp.types.override import override


@runtime_checkable
class PreferenceMenuNameProtocol(Protocol):
    __cvp_menu_name__: str


class PreferenceInterface(ABC):
    @classmethod
    @abstractmethod
    def get_menu_name(cls) -> str:
        raise NotImplementedError

    @abstractmethod
    def on_preprocess(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_postprocess(self) -> None:
        raise NotImplementedError


class BasePreference(PreferenceInterface, PreferenceMenuNameProtocol, ABC):
    def __init__(self, context: Context):
        assert isinstance(self, PreferenceMenuNameProtocol)
        self._context = context

    @classmethod
    @override
    def get_menu_name(cls) -> str:
        return cls.__cvp_menu_name__

    @override
    def on_preprocess(self) -> None:
        pass

    @override
    def on_postprocess(self) -> None:
        pass

    @property
    def context(self) -> Context:
        return self._context

    def get_selected_submenu(self, *, suffix=None) -> str:
        return self._context.get_selected_submenu(type(self), suffix=suffix)

    def set_selected_submenu(self, value: str, *, suffix=None) -> None:
        self._context.set_selected_submenu(type(self), value, suffix=suffix)

    @property
    def selected_submenu(self) -> str:
        return self.get_selected_submenu()

    @selected_submenu.setter
    def selected_submenu(self, value: str) -> None:
        self.set_selected_submenu(value)
