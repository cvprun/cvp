# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional

from croniter import croniter

from cvp.variables import INFINITE


class JobState:
    def __init__(self, cronexpr: str, repeat=INFINITE):
        if not cronexpr:
            raise ValueError("Cron expression is not set for this job")

        self._counter = 0
        self._repeat = repeat
        self._cron = croniter(cronexpr)

    @property
    def cron(self) -> croniter:
        return self._cron

    def set_current(self, start: datetime, *, force=True) -> None:
        self._cron.set_current(start, force=force)

    def get_next(self, start: Optional[datetime] = None) -> datetime:
        result = self._cron.get_next(datetime, start, update_current=True)
        assert isinstance(result, datetime)
        return result

    @property
    def repeat_count(self) -> int:
        return self._counter

    def increment_repeat_count(self) -> None:
        self._counter += 1

    def clear_repeat_count(self) -> None:
        self._counter = 0

    @property
    def is_done(self) -> bool:
        if self._repeat == INFINITE:
            return False
        else:
            return self._repeat <= self._counter
