# -*- coding: utf-8 -*-

from os import PathLike
from typing import Union

from cvp.system.path import PathFlavour

from cvp.variables import DEFAULT_CHAT_SQLITE_FILENAME


class Chat(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)

    def get_database_path(self):
        return self.as_path() / DEFAULT_CHAT_SQLITE_FILENAME
