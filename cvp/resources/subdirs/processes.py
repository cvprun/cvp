# -*- coding: utf-8 -*-

from datetime import datetime
from os import PathLike
from typing import Optional, Union

from cvp.chrono.filename import short_datetime_name
from cvp.paths.flavour import PathFlavour
from cvp.variables import (
    PROCESS_LOGFILE_PREFIX,
    PROCESS_LOGFILE_SUFFIX,
    PROCESS_PIDFILE_SUFFIX,
)


class ProcessesPath(PathFlavour):
    def __init__(
        self,
        *path: Union[str, PathLike[str]],
        logfile_prefix=PROCESS_LOGFILE_PREFIX,
        logfile_suffix=PROCESS_LOGFILE_SUFFIX,
        pidfile_suffix=PROCESS_PIDFILE_SUFFIX,
    ):
        super().__init__(*path)
        self.logfile_prefix = logfile_prefix
        self.logfile_suffix = logfile_suffix
        self.pidfile_suffix = pidfile_suffix

    @staticmethod
    def generate_logfile_name(stream: str, dt: Optional[datetime] = None):
        dt = dt if dt is not None else datetime.now()
        assert dt is not None
        return f"{stream}.{short_datetime_name(dt)}"

    def generate_logfile_fullname(self, stream: str, dt: Optional[datetime] = None):
        filename = self.generate_logfile_name(stream, dt)
        return self.logfile_prefix + filename + self.logfile_suffix

    def generate_log_path(self, key: str, stream: str, dt: Optional[datetime] = None):
        return self.as_path() / key / self.generate_logfile_fullname(stream, dt)

    def get_pid_path(self, key: str):
        return self.as_path() / (key + self.logfile_suffix)
