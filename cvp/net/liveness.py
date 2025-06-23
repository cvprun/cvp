# -*- coding: utf-8 -*-

from threading import Lock, Thread
from typing import Final, Optional

import requests


class ServerLivenessProbe:
    MIN_TIMEOUT: Final[float] = 1.0
    MAX_TIMEOUT: Final[float] = 120.0
    DEFAULT_TIMEOUT: Final[float] = 2.0

    _alive: Optional[bool]

    def __init__(self, address: Optional[str] = None, timeout=DEFAULT_TIMEOUT):
        if not (self.MIN_TIMEOUT <= timeout <= self.MAX_TIMEOUT):
            raise ValueError(
                f"timeout must be between {self.MIN_TIMEOUT} and {self.MAX_TIMEOUT}"
            )

        self._address = address
        self._timeout = timeout
        self._alive = None
        self._lock = Lock()

        if self._address:
            self._lock.acquire()
            self._thread = Thread(
                target=self._update,
                args=(self._lock, self._address, self._timeout),
            )
            self._thread.start()
        else:
            self._alive = False

    def _update(self, lock: Lock, address: str, timeout: float) -> None:
        try:
            try:
                requests.options(address, timeout=timeout)
                self._alive = True
            except:  # noqa
                self._alive = False
        finally:
            lock.release()

    def is_alive(self) -> bool:
        with self._lock:
            return bool(self._alive)

    @property
    def address(self):
        return self._address

    @property
    def timeout(self):
        return self._timeout
