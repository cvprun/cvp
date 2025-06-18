# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from typing import Optional


class ServiceState:
    def __init__(self, counter=0, spawned_at: Optional[datetime] = None):
        self._counter = counter
        self._spawned_at = spawned_at if spawned_at else datetime.now().astimezone()
        self._awaiting_restart = False

    @property
    def restart_count(self) -> int:
        return self._counter

    def increment_restart_count(self) -> None:
        self._counter += 1

    def clear_restart_count(self) -> None:
        self._counter = 0

    @property
    def spawned_at(self) -> datetime:
        return self._spawned_at

    @spawned_at.setter
    def spawned_at(self, value: datetime) -> None:
        self._spawned_at = value

    def update_spawn_time(self) -> None:
        self._spawned_at = datetime.now().astimezone()

    def elapsed_timedelta(self, base: Optional[datetime] = None) -> timedelta:
        if base is None:
            base = datetime.now().astimezone()
        return base - self._spawned_at

    def elapsed_seconds(self, base: Optional[datetime] = None) -> float:
        return self.elapsed_timedelta(base).total_seconds()

    @property
    def is_awaiting_restart(self) -> bool:
        return self._awaiting_restart

    def enable_awaiting_restart(self) -> None:
        self._awaiting_restart = True

    def clear_awaiting_restart(self) -> None:
        self._awaiting_restart = False
