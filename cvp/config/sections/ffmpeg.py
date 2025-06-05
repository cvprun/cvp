# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.values.proxies.callables import CallableProxyValue
from cvp.variables import (
    FFMPEG_EXECUTABLE_FILENAME,
    FFPROBE_EXECUTABLE_FILENAME,
    STREAM_LOGGING_ENCODING,
    STREAM_LOGGING_MAXSIZE,
    STREAM_LOGGING_NEWLINE_SIZE,
)


@dataclass
class FFmpegConfig:
    ffmpeg: str = FFMPEG_EXECUTABLE_FILENAME
    ffprobe: str = FFPROBE_EXECUTABLE_FILENAME

    logging_maxsize: int = STREAM_LOGGING_MAXSIZE
    logging_encoding: str = STREAM_LOGGING_ENCODING
    logging_newline_size: int = STREAM_LOGGING_NEWLINE_SIZE

    def create_ffmpeg_proxy(self):
        def _getter() -> str:
            return self.ffmpeg

        def _setter(value: str) -> None:
            self.ffmpeg = value

        return CallableProxyValue(_getter, _setter)

    def create_ffprobe_proxy(self):
        def _getter() -> str:
            return self.ffprobe

        def _setter(value: str) -> None:
            self.ffprobe = value

        return CallableProxyValue(_getter, _setter)
