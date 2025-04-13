# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.variables import MAX_PROCESS_WORKERS, MAX_THREAD_WORKERS, THREAD_POOL_PREFIX


@dataclass
class ConcurrencyConfig:
    thread_name_prefix: str = THREAD_POOL_PREFIX
    thread_workers: int = MAX_THREAD_WORKERS
    process_workers: int = MAX_PROCESS_WORKERS
