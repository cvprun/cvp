# -*- coding: utf-8 -*-

import os
from statistics import mean, stdev
from time import perf_counter
from typing import NamedTuple

from cvp.paths.types import PathLike
from cvp.units.byte import BYTES_1MB


class BenchmarkResult(NamedTuple):
    avg_time: float
    throughput_mbs: float
    std_dev: float


def benchmark_read_size(path: PathLike, chunk_size: int, iterations=1):
    times = list()
    file_size = os.path.getsize(path)

    for _ in range(iterations):
        start_time = perf_counter()

        with open(path, "rb") as f:
            bytes_read = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                bytes_read += len(chunk)

        times.append(perf_counter() - start_time)

    avg_time = mean(times)
    throughput_mbs = (file_size / BYTES_1MB) / avg_time
    std_dev = stdev(times) if len(times) > 1 else 0.0

    return BenchmarkResult(avg_time, throughput_mbs, std_dev)
