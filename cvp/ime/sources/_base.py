# -*- coding: utf-8 -*-

from abc import ABC
from typing import Protocol, runtime_checkable

from cvp.ime.interface import InputHandlerInterface
from cvp.types.override import override


@runtime_checkable
class InputHandlerNameProtocol(Protocol):
    __cvp_ime_method_name__: str
    __cvp_ime_keyboard_layout__: str
    __cvp_ime_language__: str


class BaseInputHandler(InputHandlerInterface, InputHandlerNameProtocol, ABC):
    def __init__(self):
        assert isinstance(self, InputHandlerNameProtocol)

    @override
    def get_method_name(self) -> str:
        return self.__cvp_ime_method_name__

    @override
    def get_keyboard_layout(self) -> str:
        return self.__cvp_ime_keyboard_layout__

    @override
    def get_language(self) -> str:
        return self.__cvp_ime_language__

    @override
    def get_composing(self) -> str:
        return str()
