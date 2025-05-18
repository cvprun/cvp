# -*- coding: utf-8 -*-

from threading import Lock
from typing import Optional, Tuple


class ProgressValue:
    def __init__(
        self,
        value=0,
        limit=100,
        state: Optional[str] = None,
        *,
        lock: Optional[Lock] = None,
    ):
        self._value = value
        self._limit = limit
        self._state = state if state else str()
        self._lock = lock if lock else Lock()

    @property
    def value(self) -> int:
        with self._lock:
            return self._value

    @value.setter
    def value(self, value: int) -> None:
        with self._lock:
            self._value = value

    @property
    def limit(self) -> int:
        with self._lock:
            return self._limit

    @limit.setter
    def limit(self, limit: int) -> None:
        with self._lock:
            self._limit = limit

    @property
    def state(self) -> str:
        with self._lock:
            return self._state

    @state.setter
    def state(self, state: str) -> None:
        with self._lock:
            self._state = state

    @property
    def percentage(self) -> float:
        with self._lock:
            return self._value / self._limit

    def set(
        self,
        value: int,
        *,
        limit: Optional[int] = None,
        state: Optional[str] = None,
    ) -> None:
        with self._lock:
            self._value = value
            if limit is not None:
                self._limit = limit
            if state is not None:
                self._state = state

    def get(self) -> Tuple[int, int, str]:
        with self._lock:
            return self._value, self._limit, self._state
