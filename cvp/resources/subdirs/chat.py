# -*- coding: utf-8 -*-

from os import PathLike
from typing import Union

from cvp.paths.flavour import PathFlavour
from cvp.variables import CHAT_SQLITE_FILENAME


class ChatPath(PathFlavour):
    def __init__(self, *path: Union[str, PathLike[str]]):
        super().__init__(*path)

    def get_database_path(self):
        return self.as_path() / CHAT_SQLITE_FILENAME
