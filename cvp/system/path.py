# -*- coding: utf-8 -*-

import sys
from os import PathLike
from pathlib import Path
from typing import Union


class PathFlavour(Path):
    # noinspection PyProtectedMember
    _flavour = Path()._flavour  # type: ignore[attr-defined]

    def __init__(self, *args):
        if sys.version_info >= (3, 12):
            super().__init__(*args)
        else:
            super().__init__()

    def as_path(self):
        return Path(self)

    @classmethod
    def classname_subdir(cls, parent: Union[str, PathLike[str]]):
        return cls(Path(parent) / cls.__name__.lower())

    if sys.version_info >= (3, 12):

        def __truediv__(self, other):
            return self.__class__(self.as_path() / other)
