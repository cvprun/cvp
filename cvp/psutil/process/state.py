# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from functools import lru_cache
from typing import Annotated, Dict, List, get_args, get_origin, get_type_hints

import psutil

from cvp.variables import UNKNOWN_PID


@dataclass
class ProcessState:
    pid: Annotated[int, "PID"] = UNKNOWN_PID
    ppid: Annotated[int, "Parent PID"] = UNKNOWN_PID
    name: Annotated[str, "Name"] = field(default_factory=str)
    status: Annotated[str, "Status"] = field(default_factory=str)
    cmdline: Annotated[List[str], "Command-line"] = field(default_factory=list)
    # net_connections
    cpu_affinity: Annotated[List[int], "CPU Affinity"] = field(default_factory=list)
    cpu_num: Annotated[int, "CPU Number"] = 0
    cpu_percent: Annotated[float, "CPU Percent"] = 0.0
    # cpu_times
    create_time: Annotated[datetime, "Create Time"] = field(
        default_factory=lambda: datetime.now().astimezone(),
    )
    cwd: Annotated[str, "CWD"] = field(default_factory=str)
    # environ
    exe: Annotated[str, "EXE"] = field(default_factory=str)
    # gids
    # io_counters
    # ionice
    # memory_full_info
    # memory_info
    # memory_maps
    # memory_percent
    nice: Annotated[int, "Nice"] = 0
    num_threads: Annotated[int, "Threads"] = 0
    # open_files
    # num_ctx_switches
    # num_fds
    # num_handles
    # terminal
    # threads
    # uids
    username: Annotated[str, "username"] = field(default_factory=str)

    @classmethod
    def from_process(cls, proc: psutil.Process):
        return cls(
            pid=proc.pid,
            ppid=proc.ppid(),
            name=proc.name(),
            status=proc.status(),
            cmdline=proc.cmdline(),
            cpu_affinity=list(proc.cpu_affinity() or ()),
            cpu_num=proc.cpu_num(),
            cpu_percent=proc.cpu_percent(),
            # cpu_times=proc.cpu_times(), # user, system, children_user, children_system
            create_time=datetime.fromtimestamp(proc.create_time()).astimezone(),
            cwd=proc.cwd(),
            exe=proc.exe(),
            nice=proc.nice(),
            num_threads=proc.num_threads(),
            username=proc.username(),
        )

    @classmethod
    def from_pid(cls, pid: int):
        return cls.from_process(psutil.Process(pid))


@lru_cache
def get_process_info_field_titles() -> Dict[str, str]:
    result = dict()
    hints = get_type_hints(ProcessState, include_extras=True)
    for key, field_type in hints.items():
        if get_origin(field_type) is Annotated:
            args = get_args(field_type)
            title = args[1]
            assert isinstance(title, str)
            result[key] = title
    return result
