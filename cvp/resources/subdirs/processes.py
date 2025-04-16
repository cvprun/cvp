# -*- coding: utf-8 -*-

from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import Optional, Union

from cvp.chrono.filename import short_datetime_name
from cvp.system.path import PathFlavour


class ProcessesPath(PathFlavour):
    def __init__(self, *path: Union[str, PathLike[str]]):
        super().__init__(*path)
        self.logfile_prefix = ""
        self.logfile_suffix = ".log"

    @staticmethod
    def gen_filename(stream: str, dt: Optional[datetime] = None):
        dt = dt if dt is not None else datetime.now()
        assert dt is not None
        return f"{stream}.{short_datetime_name(dt)}"

    def gen(self, key: str, stream: str, dt: Optional[datetime] = None):
        filename = self.gen_filename(stream, dt)
        fullname = self.logfile_prefix + filename + self.logfile_suffix
        return Path(self) / key / fullname
