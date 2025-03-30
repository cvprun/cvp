# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

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
