# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from os import PathLike
from typing import List, Union

from cvp.chrono.filename import short_datetime_name
from cvp.system.path import PathFlavour


class LayoutsPath(PathFlavour):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path)
        self._prefix = "layout-"
        self._extension = ".ini"

    @property
    def extension(self):
        return self._extension

    def get_filename(self, dt: datetime) -> str:
        return self._prefix + short_datetime_name(dt) + self._extension

    def get_nonexistent_filename(self) -> str:
        dt = datetime.now().astimezone()
        while True:
            filename = self.get_filename(dt)
            if (self / filename).exists():
                dt += timedelta(seconds=1)
                continue
            return filename

    def find_layout_filepaths(self) -> List[str]:
        return self._find_files_with_extensions(self._extension, join_dirpath=True)

    def find_layout_filenames(self) -> List[str]:
        return self._find_files_with_extensions(self._extension, join_dirpath=False)
