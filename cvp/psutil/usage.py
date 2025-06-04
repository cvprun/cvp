# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional

from psutil import cpu_percent, virtual_memory

from cvp.patterns.interval import IntervalUpdater
from cvp.types.override import override


class Percentage(NamedTuple):
    cpu: float
    vmem: float


def query_system_usage():
    return Percentage(cpu_percent(interval=None), virtual_memory().percent)


class SystemUsage(IntervalUpdater[Percentage]):
    def __init__(self, interval: Optional[float] = None):
        super().__init__(initial=query_system_usage(), interval=interval)

    @override
    def on_update(self) -> Percentage:
        return query_system_usage()
