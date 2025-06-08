# -*- coding: utf-8 -*-

import io
import os
from argparse import Namespace
from signal import SIGINT
from subprocess import DEVNULL, Popen
from typing import IO, Callable, Iterable, Mapping, Optional, Sequence, Tuple, Union

import psutil

from cvp.process.flags import default_creation_flags
from cvp.process.status import ProcessStatusEx
from cvp.process.stream import StreamBufferPair


class ProcessInit(Namespace):
    args: Sequence[str]
    buffer_size: Optional[int]
    stdin: Optional[Union[int, IO]]
    stdout: Optional[Union[int, IO]]
    stderr: Optional[Union[int, IO]]
    cwd: Optional[Union[str, os.PathLike[str]]]
    env: Optional[Union[Mapping[str, str], Mapping[bytes, bytes]]]
    creation_flags: Optional[int]
    name: Optional[str]
    pass_fds: Optional[Iterable[int]]
    user: Optional[Union[str, str]]
    group: Optional[Union[str, str]]
    extra_groups: Optional[Iterable[Union[str, int]]]
    encoding: Optional[str]
    errors: Optional[str]
    text: Optional[bool]
    umask: Optional[int]
    pipe_size: Optional[int]
    process_group: Optional[int]


class Process:
    def __init__(
        self,
        args: Sequence[str],
        buffer_size: Optional[int] = None,
        stdin: Optional[Union[int, IO]] = None,
        stdout: Optional[Union[int, IO]] = DEVNULL,
        stderr: Optional[Union[int, IO]] = DEVNULL,
        cwd: Optional[Union[str, os.PathLike[str]]] = None,
        env: Optional[Union[Mapping[str, str], Mapping[bytes, bytes]]] = None,
        creation_flags: Optional[int] = None,
        name: Optional[str] = None,
        pass_fds: Optional[Iterable[int]] = None,
        user: Optional[Union[str, str]] = None,
        group: Optional[Union[str, str]] = None,
        extra_groups: Optional[Iterable[Union[str, int]]] = None,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        text: Optional[bool] = None,
        umask: Optional[int] = None,
        pipe_size: Optional[int] = None,
        process_group: Optional[int] = None,
        *,
        stream_buffers: Optional[StreamBufferPair] = None,
        teardown: Optional[Callable[..., None]] = None
    ):
        self._init = Namespace(
            args=args,
            buffer_size=buffer_size,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            cwd=cwd,
            env=env,
            creation_flags=creation_flags,
            name=name,
        )

        if buffer_size is None:
            buffer_size = io.DEFAULT_BUFFER_SIZE
        if creation_flags is None:
            creation_flags = default_creation_flags()

        assert isinstance(buffer_size, int)
        assert isinstance(creation_flags, int)

        # https://docs.python.org/3.13/library/subprocess.html
        self._popen = Popen(
            args,
            bufsize=buffer_size,
            executable=None,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            preexec_fn=None,
            close_fds=True,
            shell=False,
            cwd=cwd,
            env=env,
            universal_newlines=None,
            startupinfo=None,
            creationflags=creation_flags,
            restore_signals=True,
            start_new_session=False,
            pass_fds=tuple(pass_fds or ()),
            user=user,
            group=group,
            # extra_groups=extra_groups or None,
            # encoding=encoding,
            # errors=errors,
            # text=text,
            # umask=umask or -1,
            # pipesize=pipe_size or -1,
            process_group=process_group,
        )
        assert self._popen.pid != 0
        self._psutil = psutil.Process(self._popen.pid)
        self._stream_buffers = stream_buffers
        self._teardown = teardown

    @classmethod
    def from_namespace(cls, init: ProcessInit):
        return cls(
            args=init.args,
            buffer_size=init.buffer_size,
            stdin=init.stdin,
            stdout=init.stdout,
            stderr=init.stderr,
            cwd=init.cwd,
            env=init.env,
            creation_flags=init.creation_flags,
            name=init.name,
            pass_fds=init.pass_fds,
            user=init.user,
            group=init.group,
            extra_groups=init.extra_groups,
            encoding=init.encoding,
            errors=init.errors,
            text=init.text,
            umask=init.umask,
            pipe_size=init.pipe_size,
            process_group=init.process_group,
        )

    @property
    def namespace(self):
        return self._init

    @property
    def name(self):
        return self._init.name

    @property
    def psutil(self):
        return self._psutil

    @property
    def pid(self) -> int:
        return self._popen.pid

    @property
    def returncode(self) -> int:
        return self._popen.returncode

    @property
    def stdin(self):
        return self._popen.stdin

    @property
    def stdout(self):
        return self._popen.stdout

    @property
    def stderr(self):
        return self._popen.stderr

    @property
    def stdout_buffer(self):
        return self._stream_buffers.stdout if self._stream_buffers is not None else None

    @property
    def stderr_buffer(self):
        return self._stream_buffers.stderr if self._stream_buffers is not None else None

    @property
    def args(self):
        return self._popen.args

    def poll(self) -> Optional[int]:
        return self._popen.poll()

    def wait(self, timeout: Optional[float] = None) -> int:
        return self._popen.wait(timeout)

    def communicate(
        self,
        data: Optional[bytes] = None,
        timeout: Optional[float] = None,
    ) -> Tuple[Optional[bytes], Optional[bytes]]:
        # [WARNING]
        # The data read is buffered in memory,
        # so do not use this method if the data size is large or unlimited.
        stdout, stderr = self._popen.communicate(data, timeout)
        assert isinstance(stdout, (type(None), bytes))
        assert isinstance(stderr, (type(None), bytes))
        return stdout, stderr

    def send_signal(self, signum: int) -> None:
        self._popen.send_signal(signum)

    def interrupt(self) -> None:
        self._popen.send_signal(SIGINT)

    def terminate(self) -> None:
        self._popen.terminate()

    def kill(self) -> None:
        self._popen.kill()

    def is_alive(self) -> bool:
        return self._popen.poll() is None

    def status(self) -> ProcessStatusEx:
        if self._popen.poll() is None:
            try:
                return ProcessStatusEx(self._psutil.status())
            except psutil.NoSuchProcess:
                return ProcessStatusEx.no_such
        else:
            return ProcessStatusEx.exited

    def teardown(self):
        if self._stream_buffers is not None:
            self._stream_buffers.close()
            self._stream_buffers = None

        if self._teardown is not None:
            self._teardown()
            self._teardown = None
