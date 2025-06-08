# -*- coding: utf-8 -*-

import io
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from enum import StrEnum, auto, unique
from getpass import getuser
from grp import getgrgid
from pathlib import Path
from typing import Callable, Dict, Final, List, NewType, Optional, Union
from uuid import uuid4

from cvp.paths.normalize import normalize_path
from cvp.process.flags import default_creation_flags
from cvp.strings.joins import join_iterable
from cvp.variables import (
    COMMA,
    NEWLINE,
    STDERR_FILE_HANDLE,
    STDERR_FILE_NAME,
    STDIN_FILE_HANDLE,
    STDIN_FILE_NAME,
    STDOUT_FILE_HANDLE,
    STDOUT_FILE_NAME,
)

ServiceKey = NewType("ServiceKey", str)

USE_SYSTEM_DEFAULT_BUFFER: Final[int] = -1
USE_UNBUFFERED: Final[int] = 0
USE_LINE_BUFFERED: Final[int] = 1


@unique
class RestartPolicy(StrEnum):
    """
    To configure the restart policy for a service.
    """

    none = auto()
    """
    Don't automatically restart the service.
    """

    on_failure = auto()
    """
    Restart the service if it exits due to an error,
    which manifests as a success exit codes.
    """

    always = auto()
    """
    Always restart the service if it stops.
    """


@dataclass
class StreamInfo:
    type: int
    handle: Optional[int] = None
    file: str = field(default_factory=str)

    @classmethod
    def from_stdin(cls):
        assert 0 == STDIN_FILE_HANDLE
        return cls(STDIN_FILE_HANDLE, subprocess.DEVNULL)

    @classmethod
    def from_stdout(cls):
        assert 1 == STDOUT_FILE_HANDLE
        return cls(STDOUT_FILE_HANDLE, subprocess.DEVNULL)

    @classmethod
    def from_stderr(cls):
        assert 2 == STDERR_FILE_HANDLE
        return cls(STDERR_FILE_HANDLE, subprocess.DEVNULL)

    @property
    def is_stdin(self) -> bool:
        return self.type == STDIN_FILE_HANDLE

    @property
    def is_stdout(self) -> bool:
        return self.type == STDOUT_FILE_HANDLE

    @property
    def is_stderr(self) -> bool:
        return self.type == STDERR_FILE_HANDLE

    @property
    def name(self) -> str:
        match self.type:
            case 0:
                return STDIN_FILE_NAME
            case 1:
                return STDOUT_FILE_NAME
            case 2:
                return STDERR_FILE_NAME
            case _:
                assert False, "Inaccessible section"

    @property
    def is_pipe(self) -> bool:
        """
        Special value that can be used as the stdin, stdout or stderr argument to
        `Popen` and indicates that a pipe to the standard stream should be opened.
        Most useful with `Popen.communicate()`.
        """
        return self.handle == subprocess.PIPE

    @property
    def is_same_standard_output(self) -> bool:
        """
        Special value that can be used as the stderr argument to `Popen` and indicates
        that standard error should go into the same handle as standard output.
        """
        return self.handle == subprocess.STDOUT

    @property
    def is_devnull(self) -> bool:
        """
        Special value that can be used as the stdin, stdout or stderr argument to
        `Popen` and indicates that the special file `os.devnull` will be used.
        """
        return self.handle == subprocess.DEVNULL

    @property
    def is_same_type(self) -> bool:
        return self.handle == self.type

    @property
    def is_handle(self) -> bool:
        return self.handle is not None

    @property
    def is_file(self) -> bool:
        return not self.is_handle

    def set_file(self, file: Optional[str] = None) -> None:
        self.handle = None
        self.file = file if file else str()

    def set_pipe(self) -> None:
        self.handle = subprocess.PIPE

    def set_same_standard_output(self) -> None:
        self.handle = subprocess.STDOUT

    def set_devnull(self) -> None:
        self.handle = subprocess.DEVNULL

    def set_default_stream_number(self) -> None:
        self.handle = self.type

    def set_handle(self, value: int) -> None:
        self.handle = value

    def set_none_handle(self) -> None:
        self.handle = None

    def open(
        self,
        *,
        path_generator: Optional[Callable[[], str]] = None,
        mode=0o600,
    ) -> int:
        if self.is_handle:
            assert self.handle is not None
            return self.handle

        assert self.is_file
        assert self.handle is None

        if self.file:
            file = self.file
        elif path_generator:
            file = path_generator()
        else:
            raise ValueError("No file source specified")

        if self.is_stdin:
            if not os.path.exists(file):
                os.close(os.open(file, os.O_WRONLY | os.O_CREAT, mode))
            flags = os.O_RDONLY
        else:
            flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC

        return os.open(file, flags, mode)


@dataclass
class ServiceItem:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)

    managed: bool = False
    freeze: bool = False
    enabled: bool = False

    executable: str = field(default_factory=lambda: sys.executable)
    args: str = field(default_factory=str)

    buffer_size: int = USE_SYSTEM_DEFAULT_BUFFER
    """Specifies the buffer size used when creating pipe file objects for stdio.

    The value is passed as the `buffering` argument to the `open()` function for
    stdin, stdout, and stderr.

    - 0: unbuffered (each read/write is a single system call and may return short)
    - 1: line buffered (only valid if `text=True` or `universal_newlines=True`)
    - >1: use a buffer of approximately that size
    - <0: use system default (`io.DEFAULT_BUFFER_SIZE`)
    """

    stdin: StreamInfo = field(default_factory=lambda: StreamInfo.from_stdin())
    stdout: StreamInfo = field(default_factory=lambda: StreamInfo.from_stdout())
    stderr: StreamInfo = field(default_factory=lambda: StreamInfo.from_stderr())

    cwd: str = field(default_factory=lambda: str(Path.home()))
    env: Dict[str, str] = field(default_factory=dict)
    creation_flags: int = field(default_factory=default_creation_flags)

    pass_fds: List[int] = field(default_factory=list)
    user: str = field(default_factory=getuser)
    group: str = field(default_factory=lambda: getgrgid(os.getgid()).gr_name)
    extra_groups: List[str] = field(default_factory=list)
    encoding: str = field(default_factory=str)
    errors: str = field(default_factory=str)
    text: bool = False
    umask: int = -1
    pipe_size: int = -1
    process_group: int = -1

    restart: str = field(default_factory=str)
    restart_delay: float = 1.0
    restart_max_attempts: int = 1

    success_exit_codes: List[int] = field(default_factory=lambda: [0])

    base_class: str = field(default_factory=str)
    base_class_kwargs: Dict[str, str] = field(default_factory=dict)

    pid_file: str = field(default_factory=str)

    @property
    def key(self):
        return ServiceKey(self.uuid)

    @key.setter
    def key(self, value: ServiceKey) -> None:
        self.uuid = str(value)

    def normalize_executable(self) -> str:
        return normalize_path(self.executable)

    def set_arguments(self, value: List[str]) -> None:
        self.args = shlex.join(value)

    def split_arguments(self) -> List[str]:
        return shlex.split(self.args)

    def split_normalize_arguments(self) -> List[str]:
        return [os.path.expandvars(arg) for arg in self.split_arguments()]

    def split_normalize_commands(self) -> List[str]:
        arguments = self.split_normalize_arguments()
        if self.executable:
            return [self.normalize_executable()] + arguments
        else:
            return arguments

    def multiline_normalize_arguments(self) -> str:
        return join_iterable(self.split_normalize_arguments(), delimiter=NEWLINE)

    @property
    def normalize_commands(self) -> List[str]:
        try:
            return self.split_normalize_commands()
        except ValueError:
            # e.g. "No closing quotation"
            return list()

    def set_unbuffered(self) -> None:
        self.buffer_size = USE_UNBUFFERED

    def set_line_buffered(self) -> None:
        self.buffer_size = USE_LINE_BUFFERED

    def set_system_default_buffer(self) -> None:
        self.buffer_size = USE_SYSTEM_DEFAULT_BUFFER

    def set_default_buffer_size(self) -> None:
        self.buffer_size = io.DEFAULT_BUFFER_SIZE

    def set_user_name(self) -> None:
        self.user = getuser()

    def set_user_id(self) -> None:
        self.user = str(os.getuid())

    def set_group_id(self) -> None:
        self.group = str(os.getgid())

    def set_group_name(self) -> None:
        self.group = getgrgid(os.getgid()).gr_name

    @property
    def restart_policy(self):
        try:
            return RestartPolicy(self.restart)
        except:  # noqa
            return RestartPolicy.none

    @restart_policy.setter
    def restart_policy(self, value: Union[RestartPolicy, str]) -> None:
        try:
            if isinstance(value, RestartPolicy):
                self.restart = str(value)
            else:
                assert isinstance(value, str)
                self.restart = str(RestartPolicy(value))
        except:  # noqa
            self.restart = str(RestartPolicy.none)

    def join_success_exit_codes(self) -> str:
        return join_iterable(self.success_exit_codes, delimiter=COMMA)

    @staticmethod
    def split_success_exit_codes(value: str) -> List[int]:
        items = filter(lambda x: x.strip(), value.split(sep=COMMA))
        codes = map(lambda x: int(x), items)
        return list(codes)

    @property
    def is_text_mode(self) -> bool:
        return bool(self.encoding or self.errors or self.text)
