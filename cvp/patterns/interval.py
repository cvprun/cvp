# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from time import time
from typing import Callable, Generic, Optional, TypeVar

from cvp.types.override import override

ResultT = TypeVar("ResultT")


class IntervalUpdaterInterface(Generic[ResultT], ABC):
    @abstractmethod
    def on_update(self) -> ResultT:
        raise NotImplementedError


class IntervalUpdater(IntervalUpdaterInterface[ResultT]):
    def __init__(
        self,
        initial: ResultT,
        interval: Optional[float] = None,
        updater: Optional[Callable[[], ResultT]] = None,
    ):
        self.result = initial
        self.interval = interval
        self.updater = updater
        self.latest_time = time()

    @override
    def on_update(self) -> ResultT:
        if self.updater is not None:
            return self.updater()
        else:
            raise NotImplementedError

    def update(self, update_time: Optional[float] = None) -> ResultT:
        self.latest_time = update_time if update_time is not None else time()
        self.result = self.on_update()
        return self.result

    def get(self) -> ResultT:
        current = time()

        if self.interval is not None:
            if current - self.latest_time < self.interval:
                return self.result

        return self.update(current)
