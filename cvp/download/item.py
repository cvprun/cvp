# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class DownloadItem:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    url: str = field(default_factory=str)
    size: int = -1
    error: str = field(default_factory=str)
    created_at: datetime = field(default_factory=lambda: datetime.now().astimezone())

    @property
    def has_error(self) -> bool:
        return bool(self.error)
