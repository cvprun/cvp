# -*- coding: utf-8 -*-

import os
import sys
from os import PathLike
from pathlib import Path
from typing import Final, List, Union


class PathFlavour(Path):
    _SUBCLASS_NAME_SUFFIX: Final[str] = "Path"

    # noinspection PyProtectedMember
    _flavour = Path()._flavour  # type: ignore[attr-defined]

    def __init__(self, *args):
        if sys.version_info >= (3, 12):
            super().__init__(*args)
        else:
            super().__init__()

    def as_path(self):
        return Path(self)

    def walk_with_extensions(
        self,
        *extensions: str,
        ignore_case=False,
        join_dirpath=False,
    ) -> List[str]:
        result = list()
        if ignore_case:
            extensions = tuple(e.lower() for e in extensions)
        for dirpath, dirnames, filenames in self.walk():
            for filename in filenames:
                ext = os.path.splitext(filename)[1]
                if ignore_case:
                    ext = ext.lower()
                if ext in extensions:
                    if join_dirpath:
                        result.append(os.path.join(dirpath, filename))
                    else:
                        result.append(filename)
        return result

    def list_first_depth_filepaths(self, *extensions: str, ignore_case=False):
        result = list()
        if ignore_case:
            extensions = tuple(e.lower() for e in extensions)
        for path in self.iterdir():
            if not path.is_file():
                continue
            suffix = path.suffix.lower() if ignore_case else path.suffix
            if suffix in extensions:
                result.append(path)
        return result

    def list_first_depth_filenames(self, *extensions: str, ignore_case=False):
        paths = self.list_first_depth_filepaths(*extensions, ignore_case=ignore_case)
        return list(path.name for path in paths)

    def list_first_depth_dirpaths(self):
        return list(path for path in self.iterdir() if path.is_dir())

    def list_first_depth_dirnames(self):
        paths = self.list_first_depth_dirpaths()
        return list(path.name for path in paths)

    @classmethod
    def get_subdir_name(cls) -> str:
        if not cls.__name__.endswith(cls._SUBCLASS_NAME_SUFFIX):
            raise TypeError(
                f"Class name must end with '{cls._SUBCLASS_NAME_SUFFIX}', "
                f"got '{cls.__name__}'"
            )

        dirname = cls.__name__.removesuffix(cls._SUBCLASS_NAME_SUFFIX).lower()
        assert not dirname.endswith(cls._SUBCLASS_NAME_SUFFIX.lower())
        return dirname

    @classmethod
    def classname_subdir(cls, parent: Union[str, PathLike[str]]):
        return cls(Path(parent) / cls.get_subdir_name())

    if (3, 12) <= sys.version_info:

        def __truediv__(self, other):
            return self.__class__(self.as_path() / other)
