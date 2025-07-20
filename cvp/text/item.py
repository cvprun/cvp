# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import NewType
from uuid import uuid4

TextKey = NewType("TextKey", str)


@dataclass
class TextItem:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    path: str = field(default_factory=str)
    encoding: str = "utf-8"
    errors: str = "strict"

    @property
    def key(self):
        return TextKey(self.uuid)

    @key.setter
    def key(self, value: TextKey) -> None:
        self.uuid = str(value)

    @property
    def is_memory(self) -> bool:
        return not self.path
