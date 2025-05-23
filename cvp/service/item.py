# -*- coding: utf-8 -*-

import io
from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from subprocess import DEVNULL, PIPE, STDOUT
from typing import Dict, List, NewType, Optional
from uuid import uuid4

from cvp.process.flags import default_creation_flags
from cvp.variables import STDERR_FILE_HANDLE, STDIN_FILE_HANDLE, STDOUT_FILE_HANDLE

ServiceKey = NewType("ServiceKey", str)


@unique
class RestartCondition(StrEnum):
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
    args: List[str] = field(default_factory=list)
    buffer_size: int = io.DEFAULT_BUFFER_SIZE
    stdin: StreamInfo = field(default_factory=StreamInfo)
    stdout: StreamInfo = field(default_factory=StreamInfo)
    stderr: StreamInfo = field(default_factory=StreamInfo)
    cwd: str = field(default_factory=str)
    env: Dict[str, str] = field(default_factory=dict)
    creation_flags: int = field(default_factory=default_creation_flags)
    name: str = field(default_factory=str)

    user: str = field(default_factory=str)
    group: str = field(default_factory=str)

    restart_policy: str = field(default_factory=str)
    restart_delay: float = 1.0
    restart_max_attempts: int = 1

    success_exit_status: List[int] = field(default_factory=list)

    base_class: str = field(default_factory=str)
    base_class_kwargs: Dict[str, str] = field(default_factory=dict)

    exec_start_pre: List[str] = field(default_factory=list)
    exec_start_post: List[str] = field(default_factory=list)
    exec_reload: List[str] = field(default_factory=list)
    exec_stop: List[str] = field(default_factory=list)
    exec_stop_post: List[str] = field(default_factory=list)

    pid_file: str = field(default_factory=str)

    @property
    def key(self):
        return ServiceKey(self.uuid)

    @key.setter
    def key(self, value: ServiceKey) -> None:
        self.uuid = str(value)

    @property
    def restart_condition(self):
        try:
            return RestartCondition(self.restart_policy)
        except:  # noqa
            return RestartCondition.none

    @restart_condition.setter
    def restart_condition(self, value: RestartCondition) -> None:
        try:
            self.restart_policy = str(value)
        except:  # noqa
            self.restart_policy = str(RestartCondition.none)
