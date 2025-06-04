# -*- coding: utf-8 -*-

import os.path
from typing import Dict, Mapping, Optional, Sequence, Tuple, Union
from uuid import uuid4
from weakref import ReferenceType, ref

from cvp.config.sections.ffmpeg import FFmpegConfig
from cvp.gl.textures.texture import Texture
from cvp.logging.loggers import logger
from cvp.media.config import MediaConfig, MediaKey
from cvp.media.process.frame import FrameReaderProcess, FrameShape
from cvp.media.process.spawn import spawn_frame_reader_process
from cvp.net.uri.parser import is_file_scheme
from cvp.process.mapper import ProcessMapper
from cvp.resources.manager.manager import ResourceManager
from cvp.resources.subdirs.medias import MediasPath
from cvp.resources.subdirs.processes import ProcessesPath
from cvp.variables import (
    MEDIA_FRAME_PIPE_STDOUT,
    MEDIA_FRAME_RGB24_CHANNELS,
    MEDIA_NONAME,
)


class MediaManager(ResourceManager[MediaKey, MediaConfig]):
    _config: ReferenceType[FFmpegConfig]
    _processes: ProcessMapper[MediaKey, FrameReaderProcess]
    _textures: Dict[MediaKey, Texture]

    def __init__(
        self,
        medias_path: MediasPath,
        processes_path: ProcessesPath,
        config: FFmpegConfig,
        *,
        reload=False,
        raise_errors=False,
    ):
        super().__init__(
            key_type=MediaKey,
            config_type=MediaConfig,
            root_dir=medias_path,
            reload=reload,
            raise_errors=raise_errors,
        )
        self._processes_path = processes_path
        self._config = ref(config)
        self._processes = ProcessMapper()
        self._textures = dict()

    @property
    def ffmpeg_config(self) -> FFmpegConfig:
        config = self._config()
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

    def add_media(
        self,
        name=MEDIA_NONAME,
        *,
        uuid: Optional[str] = None,
    ) -> Tuple[MediaKey, MediaConfig]:
        if not uuid:
            uuid = str(uuid4())
        assert isinstance(uuid, str)

        config = MediaConfig(uuid=uuid, name=name)
        assert uuid == str(config.key)

        self.add(config.key, config)
        return config.key, config

    def spawnable(self, key: MediaKey) -> bool:
        return self._processes.spawnable(key)

    def stoppable(self, key: MediaKey) -> bool:
        return self._processes.stoppable(key)

    def removable(self, key: MediaKey) -> bool:
        return self._processes.removable(key)

    def status(self, key: MediaKey):
        return self._processes.status(key)

    def interrupt(self, key: MediaKey) -> None:
        return self._processes.interrupt(key)

    def removable_pop(self, key: MediaKey):
        process = self._processes.removable_pop(key)
        texture = self._textures.pop(key)
        assert texture.opened
        texture.close()
        return process

    def shutdown(self, timeout: Optional[float] = None):
        self._processes.shutdown(timeout)

    @property
    def processes(self):
        return self._processes

    def get_process(self, key: MediaKey):
        return self._processes.get(key)

    def get_texture(self, key: MediaKey):
        return self._textures.get(key)

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
            stderr_path=self._processes_path.generate_log_path(name, "stderr"),
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

    def _spawn_with_file(self, key: MediaKey, file: str, width: int, height: int):
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

    def _spawn_with_rtsp(self, key: MediaKey, url: str, width: int, height: int):
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

    def _spawn_with_auto(self, key: MediaKey, file: str, width: int, height: int):
        if os.path.isfile(file) or is_file_scheme(file):
            return self._spawn_with_file(key, file, width, height)
        else:
            return self._spawn_with_rtsp(key, file, width, height)

    def spawn_ffmpeg(
        self,
        key: MediaKey,
        file: str,
        width: int,
        height: int,
    ) -> Optional[FrameReaderProcess]:
        if key in self._processes:
            raise KeyError(f"Key is exists: '{key}'")

        try:
            process = self._spawn_with_auto(key, file, width, height)
            logger.info(f"Spawned frame reader process: {process.pid}")
        except BaseException as e:
            logger.exception(e)
            return None

        assert key not in self._processes
        self._processes[key] = process

        texture = Texture()
        texture.open(width, height)
        self._textures[key] = texture

        return process

    def update_texture(self, key: MediaKey) -> int:
        process = self.get_process(key)
        if process is None:
            raise KeyError(f"Process is not exists: '{key}'")

        if process.poll() is not None:
            raise ValueError(f"Process is not alive: '{key}'")

        pixels = process.dequeue_latest()
        if not pixels:
            raise ValueError(f"Pixels is empty: '{key}'")

        texture = self.get_texture(key)
        if texture is None:
            raise KeyError(f"Texture is not exists: '{key}'")

        with texture:
            texture.update_rgb_pixels(pixels)

        return texture.texture_id

    def get_latest_texture(self, key: MediaKey) -> Optional[int]:
        try:
            return self.update_texture(key)
        except (KeyError, ValueError):
            return None
