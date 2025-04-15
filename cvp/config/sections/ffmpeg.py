# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.variables import STREAM_LOGGING_MAXSIZE, STREAM_LOGGING_NEWLINE_SIZE


@dataclass
class FFmpegConfig:
    ffmpeg: str = "ffmpeg"
    ffprobe: str = "ffprobe"

    logging_maxsize: int = STREAM_LOGGING_MAXSIZE
    logging_encoding: str = "utf-8"
    logging_newline_size: int = STREAM_LOGGING_NEWLINE_SIZE
