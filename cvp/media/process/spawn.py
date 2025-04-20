# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Mapping, Optional, Sequence, Tuple, Union

from cvp.media.process.frame import FrameReaderProcess, FrameShape
from cvp.process.stream import StreamBufferPair
from cvp.variables import (
    STREAM_LOGGING_ENCODING,
    STREAM_LOGGING_MAXSIZE,
    STREAM_LOGGING_NEWLINE_SIZE,
)


def spawn_frame_reader_process(
    name: str,
    ffmpeg_executable: str,
    ffmpeg_args: Sequence[str],
    frame_shape: Union[FrameShape | Tuple[int, int, int] | Sequence[int]],
    stderr_path: Path,
    env: Optional[Union[Mapping[str, str], Mapping[bytes, bytes]]] = None,
    start_thread=True,
    logging_encoding=STREAM_LOGGING_ENCODING,
    logging_maxsize=STREAM_LOGGING_MAXSIZE,
    logging_newline_size=STREAM_LOGGING_NEWLINE_SIZE,
):
    working_dir = stderr_path.parent
    working_dir.mkdir(parents=True, exist_ok=True)

    stream_buffers = StreamBufferPair(
        stdout=None,
        stderr=stderr_path,
        encoding=logging_encoding,
        maxsize=logging_maxsize,
        newline_size=logging_newline_size,
    )
    assert stream_buffers.stderr is not None
    stderr_fileno = stream_buffers.stderr.writable_fileno()
    assert 0 <= stderr_fileno

    process = FrameReaderProcess(
        name=name,
        args=[ffmpeg_executable] + list(ffmpeg_args),
        frame_shape=frame_shape,
        stdin=None,
        stderr=stderr_fileno,
        cwd=str(working_dir),
        env=env,
        creation_flags=None,
        target=None,
        stream_buffers=stream_buffers,
    )

    if start_thread:
        process.thread.start()

    return process
