# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import NewType
from uuid import uuid4

from cvp.scheduler.predefined import EVERY_MINUTE
from cvp.variables import INFINITE

JobKey = NewType("JobKey", str)


@dataclass
class JobItem:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default_factory=str)
    cron: str = EVERY_MINUTE
    enabled: bool = False
    managed: bool = False
    repeat: int = INFINITE

    @property
    def key(self):
        return JobKey(self.uuid)

    @key.setter
    def key(self, value: JobKey) -> None:
        self.uuid = str(value)

    def set_infinite(self) -> None:
        self.repeat = INFINITE
