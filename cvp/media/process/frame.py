# -*- coding: utf-8 -*-

import io
import os
from collections import deque
from subprocess import DEVNULL, PIPE
from threading import Lock, Thread
from typing import (
    IO,
    Callable,
    Deque,
    Mapping,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from cvp.buffers.frame import FrameBuffer
from cvp.process.process import Process
from cvp.process.stream import StreamBufferPair
from cvp.types.override import override


class FrameShape(NamedTuple):
    width: int
    height: int
    channels: int

    @property
    def size(self):
        return self.width * self.height * self.channels


class FrameReaderProcess(Process):
    _thread_error: Optional[BaseException]
    _deque: Deque[bytes]

    def __init__(
        self,
        name: str,
        args: Sequence[str],
        frame_shape: Union[FrameShape | Tuple[int, int, int] | Sequence[int]],
        stdin: Optional[Union[int, IO]] = None,
        stderr: Optional[Union[int, IO]] = DEVNULL,
        cwd: Optional[Union[str, os.PathLike[str]]] = None,
        env: Optional[Union[Mapping[str, str], Mapping[bytes, bytes]]] = None,
        creation_flags: Optional[int] = None,
        deque_maxsize=2,
        target: Optional[Callable[[bytes], None]] = None,
        *,
        stream_buffers: Optional[StreamBufferPair] = None,
        teardown: Optional[Callable[..., None]] = None
    ):
        frame_shape = FrameShape(*frame_shape)
        frame_shape_size = frame_shape.size
        if frame_shape_size <= 0:
            raise ValueError("Frame shape must be greater than zero")

        if io.DEFAULT_BUFFER_SIZE < frame_shape.size:
            buffer_size = frame_shape.size
        else:
            buffer_size = io.DEFAULT_BUFFER_SIZE

        assert isinstance(buffer_size, int)
        assert io.DEFAULT_BUFFER_SIZE <= buffer_size

        super().__init__(
            args=args,
            buffer_size=buffer_size,
            stdin=stdin,
            stdout=PIPE,
            stderr=stderr,
            cwd=cwd,
            env=env,
            creation_flags=creation_flags,
            name=name,
            stream_buffers=stream_buffers,
            teardown=teardown,
        )

        self._thread_error = None
        self._frame_shape = frame_shape
        self._target = target

        self._deque = deque(maxlen=deque_maxsize)
        self._mutex = Lock()
        self._latest = bytes()
        self._latest_count = 0

        stdout_pipe = self.stdout
        assert stdout_pipe is not None
        assert isinstance(stdout_pipe, io.BufferedReader)

        self._reader = FrameBuffer(
            pipe=stdout_pipe,
            frame_size=self._frame_shape.size,
            target=self._on_frame,
        )

        self._thread = Thread(
            group=None,
            target=self._on_read_pipe_stream_main,
            name=name,
            args=(),
            kwargs=None,
            daemon=None,
        )

    @property
    def reader(self):
        return self._reader

    @property
    def thread(self):
        return self._thread

    @property
    def thread_error(self):
        return self._thread_error

    @property
    def frame_shape(self):
        return self._frame_shape

    @property
    def latest(self):
        return self._latest

    @property
    def latest_count(self):
        return self._latest_count

    def raise_if_thread_error(self):
        if self._thread_error is not None:
            raise self._thread_error

    def _on_read_pipe_stream_main(self) -> None:
        try:
            while self.poll() is None:
                self._reader.read()

            self._reader.flush()
            self._reader.read_eof()
        except BaseException as e:
            self._thread_error = e

    def _on_frame(self, data: bytes) -> None:
        if self._target is not None:
            self._target(data)
        else:
            self.enqueue(data)

    def enqueue(self, data: bytes) -> None:
        with self._mutex:
            self._deque.append(data)

    def dequeue(self) -> bytes:
        with self._mutex:
            return self._deque.popleft()

    def dequeue_latest(self) -> bytes:
        try:
            self._latest = self.dequeue()
        except IndexError:
            # pop from an empty deque
            pass
        else:
            self._latest_count += 1

        return self._latest

    @override
    def is_alive(self) -> bool:
        if self._popen.poll() is None:
            return True
        else:
            return self._thread.is_alive()
