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

    def generate_filename(self, dt: datetime) -> str:
        return self._prefix + short_datetime_name(dt) + self._extension

    def generate_nonexistent_filename(self) -> str:
        dt = datetime.now().astimezone()
        while True:
            filename = self.generate_filename(dt)
            if (self / filename).exists():
                dt += timedelta(seconds=1)
                continue
            return filename

    def list_layout_filenames(self) -> List[str]:
        return self.list_first_depth_filenames(self._extension, ignore_case=False)
