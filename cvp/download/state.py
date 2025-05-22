# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique


@unique
class DownloadState(StrEnum):
    uninitialized = auto()
    pending = auto()
    request_content_length = auto()
    download_streaming = auto()
    verifying = auto()
    complete = auto()
