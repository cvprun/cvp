# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import List, Optional, Sequence

from cvp.ime.handlers import get_all_input_handler_types
from cvp.ime.interface import InputHandlerInterface


class ImeManager(OrderedDict[str, InputHandlerInterface]):
    def __init__(self, *handlers: InputHandlerInterface):
        super().__init__([(h.get_method_name(), h) for h in handlers])
        self._mode = list(self.keys())[0]

    @classmethod
    def from_default(cls):
        return cls(*(t() for t in get_all_input_handler_types()))

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value: str) -> None:
        self._mode = value

    @property
    def handler(self) -> InputHandlerInterface:
        return self.__getitem__(self._mode)

    def as_modes(self) -> List[str]:
        return list(self.keys())

    def change_next_mode(self) -> None:
        modes = self.as_modes()
        next_index = modes.index(self._mode) + 1
        if next_index < len(modes):
            self._mode = modes[next_index]
        else:
            self._mode = modes[0]

    def get_method_name(self) -> str:
        return self.handler.get_method_name()

    def get_keyboard_layout(self) -> str:
        return self.handler.get_keyboard_layout()

    def get_language(self) -> str:
        return self.handler.get_language()

    def has_composing(self) -> bool:
        return self.handler.has_composing()

    def get_composing(self) -> str:
        return self.handler.get_composing()

    def clear_text(self) -> None:
        self.handler.clear()

    def pop_text(self) -> Optional[str]:
        return self.handler.pop()

    def add_text(self, text: str) -> Sequence[str]:
        return self.handler.add(text)

    def flush_text(self) -> Sequence[str]:
        return self.handler.flush()
