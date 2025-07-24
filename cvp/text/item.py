# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass, field
from typing import NewType
from uuid import uuid4

from cvp.variables import TEXT_NONAME

TextKey = NewType("TextKey", str)


@dataclass
class TextItem:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    path: str = field(default_factory=str)

    encoding: str = "utf-8"
    errors: str = "strict"

    language: str = field(default_factory=str)
    palette: str = field(default_factory=str)

    show_tabs: bool = True
    show_whitespaces: bool = True

    @property
    def key(self):
        return TextKey(self.uuid)

    @key.setter
    def key(self, value: TextKey) -> None:
        self.uuid = str(value)

    @property
    def is_memory(self) -> bool:
        return not self.path

    @property
    def name(self):
        if self.path:
            return os.path.basename(self.path)
        else:
            return TEXT_NONAME

    def get_label(self, modified=False):
        return self.name + (" (*)" if modified else "") + "###" + self.uuid
