# -*- coding: utf-8 -*-

from dataclasses import dataclass
from functools import lru_cache
from typing import Annotated, Dict, List, Optional, get_args, get_origin, get_type_hints

from psutil import AccessDenied, NoSuchProcess, Process, process_iter

from cvp.patterns.interval import IntervalUpdater


@dataclass
class ProcessInfo:
    pid: Annotated[int, "PID"]
    ppid: Annotated[int, "Parent PID"]
    name: Annotated[str, "Name"]
    status: Annotated[str, "Status"]
    num_threads: Annotated[int, "Threads"]
    cmdline: Annotated[List[str], "Commandline"]

    # net_connections
    # cpu_affinity
    # cpu_num
    # cpu_percent
    # cpu_times
    # create_time
    # cwd
    # environ
    # exe
    # gids
    # io_counters
    # ionice
    # memory_full_info
    # memory_info
    # memory_maps
    # memory_percent
    # nice
    # num_ctx_switches
    # num_fds
    # num_handles
    # num_threads
    # open_files
    # num_ctx_switches
    # num_fds
    # num_handles
    # terminal
    # threads
    # uids
    # username

    @classmethod
    def from_process(cls, proc: Process):
        return cls(
            pid=proc.pid,
            ppid=proc.ppid(),
            name=proc.name(),
            status=proc.status(),
            num_threads=proc.num_threads(),
            cmdline=proc.cmdline(),
        )


@lru_cache
def get_process_info_field_titles() -> Dict[str, str]:
    result = dict()
    hints = get_type_hints(ProcessInfo, include_extras=True)
    for key, field_type in hints.items():
        if get_origin(field_type) is Annotated:
            args = get_args(field_type)
            title = args[1]
            assert isinstance(title, str)
            result[key] = title
    return result


def query_all_process_infos() -> List[ProcessInfo]:
    result = list()
    for proc in process_iter():
        try:
            result.append(ProcessInfo.from_process(proc))
        except (AccessDenied, NoSuchProcess):
            continue
    return result


class ProcessInfos(IntervalUpdater[List[ProcessInfo]]):
    def __init__(self, interval: Optional[float] = None):
        super().__init__(query_all_process_infos, interval)
