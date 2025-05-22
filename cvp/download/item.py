# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from typing import NewType, Optional, Union
from uuid import uuid4

from cvp.download.state import DownloadState
from cvp.variables import UNKNOWN_TOTAL_SIZE

DownloadKey = NewType("DownloadKey", str)


@dataclass
class DownloadItem:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    url: str = field(default_factory=str)
    dest: str = field(default_factory=str)
    timeout: Optional[float] = None
    checksum: Optional[float] = None
    follow_redirects: bool = False
    verify_ssl: bool = True

    state: DownloadState = DownloadState.uninitialized
    content_length: int = UNKNOWN_TOTAL_SIZE
    download_length: int = UNKNOWN_TOTAL_SIZE
    speed_bps: float = 0.0
    elapsed: float = 0.0
    eta: float = 0.0
    error: str = field(default_factory=str)
    created_at: datetime = field(default_factory=lambda: datetime.now().astimezone())

    @property
    def key(self):
        return DownloadKey(self.uuid)

    @key.setter
    def key(self, value: DownloadKey) -> None:
        self.uuid = str(value)

    @property
    def progress(self) -> Union[float, int]:
        if 1 <= self.content_length:
            return self.download_length / self.content_length
        else:
            return UNKNOWN_TOTAL_SIZE

    @property
    def has_error(self) -> bool:
        return bool(self.error)
