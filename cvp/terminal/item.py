# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import NewType
from uuid import uuid4

TerminalKey = NewType("TerminalKey", str)


@dataclass
class TerminalItem:
    uuid: str = field(default_factory=lambda: str(uuid4()))

    @property
    def key(self):
        return TerminalKey(self.uuid)

    @key.setter
    def key(self, value: TerminalKey) -> None:
        self.uuid = str(value)
