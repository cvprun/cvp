# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Type

from cvp.context.context import Context
from cvp.types.override import override


class PreferenceInterface(ABC):
    @classmethod
    @abstractmethod
    def get_menu_name(cls) -> str:
        raise NotImplementedError

    @abstractmethod
    def do_process(self) -> None:
        raise NotImplementedError


class BasePreference(PreferenceInterface, ABC):
    def __init__(self, context: Context):
        self._context = context

    @classmethod
    @override
    def get_menu_name(cls) -> str:
        return cls.__name__

    @property
    def context(self) -> Context:
        return self._context

    @property
    def selected_submenus(self):
        return self._context.config.preference_manager.selected_submenus

    def gen_selected_key(self, key: str) -> str:
        return type(self).__name__ + "." + key

    def get_selected(self, key: str) -> str:
        return self.selected_submenus.get(self.gen_selected_key(key), str())

    def set_selected(self, key: str, value: str) -> None:
        self.selected_submenus[self.gen_selected_key(key)] = value
