# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from time import time
from typing import Generic, Optional, TypeVar

ResultT = TypeVar("ResultT")


class IntervalUpdaterInterface(Generic[ResultT], ABC):
    @abstractmethod
    def on_update(self) -> ResultT:
        raise NotImplementedError


class IntervalUpdater(IntervalUpdaterInterface[ResultT], ABC):
    """
    A class designed for interoperability with `imgui`.

    This class is a generic abstract base class that provides automatic or manual
    data refresh functionality based on a time interval.

    This is particularly useful in situations such as:

    - Avoiding frequent updates of expensive-to-compute data.
    - Caching external data that updates periodically.
    - Scenarios where periodic (non-realtime) refresh is sufficient,
      such as API polling, sensor value caching, etc.
    """

    def __init__(
        self,
        initial: ResultT,
        interval: Optional[float] = None,
    ):
        self.result = initial
        self.interval = interval
        self.latest_time = time()

    def set_result(self, result: ResultT, update_time: Optional[float] = None) -> None:
        self.latest_time = update_time if update_time is not None else time()
        self.result = result

    def force_update(self, update_time: Optional[float] = None) -> ResultT:
        self.latest_time = update_time if update_time is not None else time()
        self.result = self.on_update()
        return self.result

    def get(self) -> ResultT:
        current = time()

        if self.interval is not None:
            if current - self.latest_time < self.interval:
                return self.result

        return self.force_update(current)
