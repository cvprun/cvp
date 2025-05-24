# -*- coding: utf-8 -*-

from datetime import datetime
from os import PathLike
from typing import Optional, Union

from cvp.chrono.filename import short_datetime_name
from cvp.paths.flavour import PathFlavour


class ProcessesPath(PathFlavour):
    def __init__(self, *path: Union[str, PathLike[str]]):
        super().__init__(*path)
        self.logfile_prefix = ""
        self.logfile_suffix = ".log"

    @staticmethod
    def generate_logfile_name(stream: str, dt: Optional[datetime] = None):
        dt = dt if dt is not None else datetime.now()
        assert dt is not None
        return f"{stream}.{short_datetime_name(dt)}"

    def generate_logfile_fullname(self, stream: str, dt: Optional[datetime] = None):
        filename = self.generate_logfile_name(stream, dt)
        return self.logfile_prefix + filename + self.logfile_suffix

    def generate(self, key: str, stream: str, dt: Optional[datetime] = None):
        return self.as_path() / key / self.generate_logfile_fullname(stream, dt)
