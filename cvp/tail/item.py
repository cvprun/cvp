# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import NewType
from uuid import uuid4

TailKey = NewType("TailKey", str)


@dataclass
class TailItem:
    uuid: str = field(default_factory=lambda: str(uuid4()))

    @property
    def key(self):
        return TailKey(self.uuid)

    @key.setter
    def key(self, value: TailKey) -> None:
        self.uuid = str(value)
