# -*- coding: utf-8 -*-

import io
import shlex
from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from subprocess import DEVNULL, PIPE, STDOUT
from typing import Dict, List, NewType, Optional
from uuid import uuid4

from cvp.process.flags import default_creation_flags
from cvp.variables import STDERR_FILE_HANDLE, STDIN_FILE_HANDLE, STDOUT_FILE_HANDLE

ServiceKey = NewType("ServiceKey", str)


@unique
class RestartPolicy(StrEnum):
    none = auto()
    on_failure = auto()
    always = auto()


@dataclass
class StreamInfo:
    value: int = DEVNULL
    file: Optional[str] = None

    @classmethod
    def from_stdin(cls):
        return cls(STDIN_FILE_HANDLE)

    @classmethod
    def from_stdout(cls):
        return cls(STDOUT_FILE_HANDLE)

    @classmethod
    def from_stderr(cls):
        return cls(STDERR_FILE_HANDLE)

    @property
    def is_pipe(self) -> bool:
        """
        Special value that can be used as the stdin, stdout or stderr argument to
        `Popen` and indicates that a pipe to the standard stream should be opened.
        Most useful with `Popen.communicate()`.
        """
        return self.value == PIPE

    @property
    def is_same_standard_output(self) -> bool:
        """
        Special value that can be used as the stderr argument to `Popen` and indicates
        that standard error should go into the same handle as standard output.
        """
        return self.value == STDOUT

    @property
    def is_devnull(self) -> bool:
        """
        Special value that can be used as the stdin, stdout or stderr argument to
        `Popen` and indicates that the special file `os.devnull` will be used.
        """
        return self.value == DEVNULL


@dataclass
class ServiceItem:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)

    cmds: str = field(default_factory=str)
    buffer_size: int = io.DEFAULT_BUFFER_SIZE
    stdin: StreamInfo = field(default_factory=StreamInfo)
    stdout: StreamInfo = field(default_factory=StreamInfo)
    stderr: StreamInfo = field(default_factory=StreamInfo)
    cwd: str = field(default_factory=str)
    env: Dict[str, str] = field(default_factory=dict)
    creation_flags: int = field(default_factory=default_creation_flags)

    user: str = field(default_factory=str)
    group: str = field(default_factory=str)

    restart: str = field(default_factory=str)
    restart_delay: float = 1.0
    restart_max_attempts: int = 1

    success_exit_status: List[int] = field(default_factory=list)

    base_class: str = field(default_factory=str)
    base_class_kwargs: Dict[str, str] = field(default_factory=dict)

    pid_file: str = field(default_factory=str)

    @property
    def key(self):
        return ServiceKey(self.uuid)

    @key.setter
    def key(self, value: ServiceKey) -> None:
        self.uuid = str(value)

    @property
    def arguments(self) -> List[str]:
        try:
            return shlex.split(self.cmds)
        except ValueError:
            return list()  # "No closing quotation"

    @arguments.setter
    def arguments(self, value: List[str]) -> None:
        self.cmds = shlex.join(value)

    @property
    def restart_policy(self):
        try:
            return RestartPolicy(self.restart)
        except:  # noqa
            return RestartPolicy.none

    @restart_policy.setter
    def restart_policy(self, value: RestartPolicy) -> None:
        try:
            self.restart = str(value)
        except:  # noqa
            self.restart = str(RestartPolicy.none)
