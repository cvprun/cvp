# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from typing import NewType
from uuid import uuid4

from croniter import croniter

from cvp.variables import INFINITE

JobKey = NewType("JobKey", str)


@dataclass
class JobItem:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)
    cron: str = field(default_factory=str)
    enabled: bool = False
    repeat: int = INFINITE

    _count: int = 0

    @property
    def repeat_count(self) -> int:
        return self._count

    def increment_repeat_count(self) -> None:
        self._count += 1

    def clear_repeat_count(self) -> None:
        self._count = 0

    @property
    def is_done(self) -> bool:
        if self.repeat == INFINITE:
            return False
        else:
            return self.repeat <= self._count

    def create_croniter(self, base: datetime):
        if not self.cron:
            raise ValueError("Cron expression is not set for this job item.")
        return croniter(self.cron, base)

    def next_schedule(self, base: datetime) -> datetime:
        return self.create_croniter(base).get_next(datetime)

    @property
    def key(self):
        return JobKey(self.uuid)

    @key.setter
    def key(self, value: JobKey) -> None:
        self.uuid = str(value)
