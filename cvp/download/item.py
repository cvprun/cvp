# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum, auto, unique
from uuid import uuid4

from cvp.variables import UNKNOWN_TOTAL_SIZE


@unique
class DownloadState(StrEnum):
    pending = auto()


@dataclass
class DownloadItem:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    url: str = field(default_factory=str)
    dest: str = field(default_factory=str)
    size: int = UNKNOWN_TOTAL_SIZE
    downloaded: int = UNKNOWN_TOTAL_SIZE
    state: DownloadState = DownloadState.pending
    progress: float = 0.0
    speed: float = 0.0
    eta: float = 0.0
    error: str = field(default_factory=str)
    created_at: datetime = field(default_factory=lambda: datetime.now().astimezone())

    @property
    def has_error(self) -> bool:
        return bool(self.error)
