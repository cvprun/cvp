# -*- coding: utf-8 -*-

from typing import Mapping, Optional, Sequence, Tuple, Union
from uuid import uuid4
from weakref import ReferenceType, ref

from cvp.config.sections.ffmpeg import FFmpegConfig
from cvp.media.config import MediaConfig
from cvp.media.process.frame import FrameShape
from cvp.media.process.spawn import spawn_frame_reader_process
from cvp.process.manager import ProcessManager
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.medias import MediasPath
from cvp.resources.subdirs.processes import ProcessesPath
from cvp.variables import (
    MEDIA_FRAME_PIPE_STDOUT,
    MEDIA_FRAME_RGB24_CHANNELS,
    MEDIA_NONAME,
)


class MediaManager(ResourceManager[MediaConfig]):
    _ffmpeg_config: ReferenceType[FFmpegConfig]

    def __init__(
        self,
        path: MediasPath,
        processes_path: ProcessesPath,
        ffmpeg_config: FFmpegConfig,
        *,
        reload=False,
        raise_errors=False,
    ):
        super().__init__(
            cls=MediaConfig,
            root_dir=path,
            reload=reload,
            raise_errors=raise_errors,
        )
        self._processes_path = processes_path
        self._ffmpeg_config = ref(ffmpeg_config)
        self._processes = ProcessManager()

    @property
    def ffmpeg_config(self) -> FFmpegConfig:
        config = self._ffmpeg_config()
        if config is None:
            raise ReferenceError("Expired ffmpeg config reference")
        return config

    @property
    def ffmpeg(self) -> str:
        return self.ffmpeg_config.ffmpeg

    @property
    def ffprobe(self) -> str:
        return self.ffmpeg_config.ffprobe

    @property
    def logging_maxsize(self) -> int:
        return self.ffmpeg_config.logging_maxsize

    @property
    def logging_encoding(self) -> str:
        return self.ffmpeg_config.logging_encoding

    @property
    def logging_newline_size(self) -> int:
        return self.ffmpeg_config.logging_newline_size

    def add_config(
        self,
        name=MEDIA_NONAME,
        *,
        uuid: Optional[str] = None,
    ) -> Tuple[str, MediaConfig]:
        uuid = uuid if uuid else str(uuid4())
        config = MediaConfig(uuid=uuid, name=name)
        self.add(uuid, config)
        return uuid, config

    def spawnable(self, key: str) -> bool:
        return self._processes.spawnable(key)

    def stoppable(self, key: str) -> bool:
        return self._processes.stoppable(key)

    def removable(self, key: str) -> bool:
        return self._processes.removable(key)

    def status(self, key: str):
        return self._processes.status(key)

    def interrupt(self, key: str) -> None:
        return self._processes.interrupt(key)

    def teardown_all(self, timeout: Optional[float] = None):
        self._processes.shutdown(timeout)

    @property
    def processes(self):
        return self._processes

    def get_process(self, key: str):
        return self._processes.get(key)

    def _spawn(
        self,
        name: str,
        ffmpeg_args: Sequence[str],
        frame_shape: Union[FrameShape | Tuple[int, int, int] | Sequence[int]],
        env: Optional[Union[Mapping[str, str], Mapping[bytes, bytes]]] = None,
        start_thread=True,
    ):
        return spawn_frame_reader_process(
            name=name,
            ffmpeg_executable=self.ffmpeg,
            ffmpeg_args=ffmpeg_args,
            frame_shape=frame_shape,
            stderr_path=self._processes_path.generate(name, "stderr"),
            env=env,
            start_thread=start_thread,
            logging_encoding=self.logging_encoding,
            logging_maxsize=self.logging_maxsize,
            logging_newline_size=self.logging_newline_size,
        )

    @staticmethod
    def alsa_default_args(stream_index=0) -> Sequence[str]:
        return "-map", f"{stream_index}:a", "-f", "alsa", "default"

    @staticmethod
    def directsound_default_args(stream_index=0) -> Sequence[str]:
        return "-map", f"{stream_index}:a", "-f", "directsound", "default"

    @staticmethod
    def rgb24_pipe_stdout_args(
        width: int,
        height: int,
        stream_index=0,
    ) -> Sequence[str]:
        return (
            "-map",
            f"{stream_index}:v",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{width}x{height}",
            MEDIA_FRAME_PIPE_STDOUT,
        )

    def _spawn_with_file(self, key: str, file: str, width: int, height: int):
        args = (
            "-hide_banner",
            "-re",
            "-i",
            file,
            *self.alsa_default_args(),
            *self.rgb24_pipe_stdout_args(width, height),
        )
        frame_shape = width, height, MEDIA_FRAME_RGB24_CHANNELS
        return self._spawn(key, args, frame_shape)

    def _spawn_with_rtsp(self, key: str, url: str, width: int, height: int):
        args = (
            "-hide_banner",
            "-fflags",
            "nobuffer",
            "-fflags",
            "discardcorrupt",
            "-flags",
            "low_delay",
            "-rtsp_transport",
            "tcp",
            "-i",
            url,
            *self.rgb24_pipe_stdout_args(width, height),
        )
        frame_shape = width, height, MEDIA_FRAME_RGB24_CHANNELS
        return self._spawn(key, args, frame_shape)

    def spawn_ffmpeg_with_file(self, key: str, file: str, width: int, height: int):
        if key in self._processes:
            raise KeyError(f"Key is exists: '{key}'")

        process = self._spawn_with_file(key, file, width, height)
        self._processes[key] = process
        return process
