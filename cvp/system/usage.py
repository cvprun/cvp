# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional

from psutil import cpu_percent, virtual_memory

from cvp.patterns.interval import IntervalUpdater


class Percentage(NamedTuple):
    cpu: float
    vmem: float


def query_system_usage():
    return Percentage(cpu_percent(interval=None), virtual_memory().percent)


class SystemUsage(IntervalUpdater[Percentage]):
    def __init__(self, interval: Optional[float] = None):
        super().__init__(query_system_usage, interval)
