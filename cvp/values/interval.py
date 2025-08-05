# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from time import time
from typing import Generic, Optional, TypeVar

ResultT = TypeVar("ResultT")


class IntervalTimer:
    def __init__(
        self,
        interval: Optional[float] = None,
        latest_time: Optional[float] = None,
    ):
        self.interval = interval if interval is not None else 0.0
        self.latest_time = latest_time if latest_time is not None else time()

    def update(self, update_time: Optional[float] = None) -> bool:
        if update_time is None:
            update_time = time()
        assert isinstance(update_time, float)

        if 0.0 < self.interval:
            if update_time - self.latest_time < self.interval:
                return False

        self.latest_time = update_time
        return True


class IntervalUpdaterInterface(Generic[ResultT], ABC):
    @abstractmethod
    def on_update(self) -> ResultT:
        raise NotImplementedError


class IntervalUpdater(IntervalTimer, IntervalUpdaterInterface[ResultT], ABC):
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
        latest_time: Optional[float] = None,
    ):
        super().__init__(interval=interval, latest_time=latest_time)
        self.result = initial

    def set_result_with_latest_time(
        self,
        result: ResultT,
        update_time: Optional[float] = None,
    ) -> None:
        self.latest_time = update_time if update_time is not None else time()
        self.result = result

    def force_update(self, update_time: Optional[float] = None) -> ResultT:
        self.latest_time = update_time if update_time is not None else time()
        self.result = self.on_update()
        return self.result

    def get(self) -> ResultT:
        update_time = time()
        if self.update(update_time):
            return self.force_update(update_time)
        else:
            return self.result
