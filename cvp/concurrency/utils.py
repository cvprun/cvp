# -*- coding: utf-8 -*-

import os
import sys
from functools import lru_cache
from typing import Final

MIN_THREAD_WORKERS: Final[int] = 5
MIN_PROCESS_WORKERS: Final[int] = 1

# On Windows, WaitForMultipleObjects is used to wait for processes to finish.
# It can wait on, at most, 63 objects. There is an overhead of two objects:
# - the result queue reader
# - the thread wakeup reader
MAX_WINDOWS_PROCESS_WORKERS: Final[int] = 63 - 2


@lru_cache
def cpu_count() -> int:
    count = os.cpu_count()
    return count if count is not None else 1


@lru_cache
def max_thread_workers() -> int:
    return min(32, cpu_count() + 4)


def valid_thread_workers(value: int) -> int:
    if value < MIN_THREAD_WORKERS:
        return MIN_THREAD_WORKERS

    max_value = max_thread_workers()
    if max_value < value:
        return max_value

    return value


def valid_process_workers(value: int) -> int:
    if value < MIN_PROCESS_WORKERS:
        return MIN_PROCESS_WORKERS

    if sys.platform == "win32" and MAX_WINDOWS_PROCESS_WORKERS < value:
        return MAX_WINDOWS_PROCESS_WORKERS

    return value
