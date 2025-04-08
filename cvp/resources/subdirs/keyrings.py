# -*- coding: utf-8 -*-

from os import PathLike
from typing import Union

from cvp.system.path import PathFlavour


class KeyringsPath(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)
