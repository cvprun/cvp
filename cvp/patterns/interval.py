# -*- coding: utf-8 -*-

from time import time
from typing import Callable, Generic, Optional, TypeVar

ResultT = TypeVar("ResultT")


class IntervalUpdater(Generic[ResultT]):
    def __init__(
        self,
        updater: Callable[[], ResultT],
        interval: Optional[float] = None,
    ):
        self.updater = updater
        self.interval = interval
        self.latest_time = time()
        self.result = updater()

    def update(self, update_time: Optional[float] = None) -> ResultT:
        self.latest_time = update_time if update_time is not None else time()
        self.result = self.updater()
        return self.result

    def get(self) -> ResultT:
        current = time()

        if self.interval is not None:
            if current - self.latest_time < self.interval:
                return self.result

        return self.update(current)
