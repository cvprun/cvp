# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum, auto, unique
from typing import NewType
from uuid import uuid4

from cvp.variables import UNKNOWN_TOTAL_SIZE

DownloadKey = NewType("DownloadKey", str)


@unique
class DownloadType(StrEnum):
    default = auto()
    curl = auto()


@unique
class DownloadState(StrEnum):
    unknown = auto()
    pending = auto()


@dataclass
class DownloadItem:
    key: DownloadKey = field(default_factory=lambda: DownloadKey(str(uuid4())))
    url: str = field(default_factory=str)
    dest: str = field(default_factory=str)
    total: int = UNKNOWN_TOTAL_SIZE
    downloaded: int = UNKNOWN_TOTAL_SIZE
    state: DownloadState = DownloadState.unknown
    progress: float = 0.0
    speed: int = 0
    elapsed: float = 0.0
    eta: float = 0.0
    error: str = field(default_factory=str)
    created_at: datetime = field(default_factory=lambda: datetime.now().astimezone())

    @property
    def has_error(self) -> bool:
        return bool(self.error)
