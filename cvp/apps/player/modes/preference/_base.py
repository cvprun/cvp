# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any

from cvp.context.context import Context
from cvp.types.override import override
from cvp.variables import MODULE_PATH_SEPARATOR


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

    def gen_selected_submenu_key(
        self,
        key: Any,
        *,
        separator=MODULE_PATH_SEPARATOR,
    ) -> str:
        return type(self).__name__ + separator + str(key)

    def get_selected_submenu(self, key: Any) -> str:
        submenu_key = self.gen_selected_submenu_key(key)
        return self.selected_submenus.get(submenu_key, str())

    def set_selected_submenu(self, key: Any, value: str) -> None:
        submenu_key = self.gen_selected_submenu_key(key)
        self.selected_submenus[submenu_key] = value
