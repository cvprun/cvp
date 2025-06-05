# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from functools import lru_cache
from types import MappingProxyType
from typing import (
    Annotated,
    Dict,
    Final,
    List,
    Optional,
    get_args,
    get_origin,
    get_type_hints,
)

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
    error: Optional[BaseException] = None

    @classmethod
    def from_process(cls, proc: psutil.Process):
        try:
            pid = proc.pid
            ppid = proc.ppid()
            name = proc.name()
            status = proc.status()
            cmdline = proc.cmdline()
            cpu_affinity = list(proc.cpu_affinity() or ())
            cpu_num = proc.cpu_num()
            cpu_percent = proc.cpu_percent()

            # cpu_times = proc.cpu_times()
            # user, system, children_user, children_system

            create_time = datetime.fromtimestamp(proc.create_time()).astimezone()
            cwd = proc.cwd()
            exe = proc.exe()
            nice = proc.nice()
            num_threads = proc.num_threads()
            username = proc.username()

            return cls(
                pid=pid,
                ppid=ppid,
                name=name,
                status=status,
                cmdline=cmdline,
                cpu_affinity=cpu_affinity,
                cpu_num=cpu_num,
                cpu_percent=cpu_percent,
                create_time=create_time,
                cwd=cwd,
                exe=exe,
                nice=nice,
                num_threads=num_threads,
                username=username,
                error=None,
            )
        except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
            return cls(error=e)

    @classmethod
    def from_pid(cls, pid: int):
        if pid == UNKNOWN_PID:
            return cls()
        else:
            return cls.from_process(psutil.Process(pid))


def _create_process_state_field_titles() -> Dict[str, str]:
    result = dict()
    hints = get_type_hints(ProcessState, include_extras=True)
    for key, field_type in hints.items():
        if get_origin(field_type) is Annotated:
            args = get_args(field_type)
            title = args[1]
            assert isinstance(title, str)
            result[key] = title
    return result


@lru_cache()
def _process_state_field_titles() -> MappingProxyType[str, str]:
    return MappingProxyType(_create_process_state_field_titles())


PROCESS_STATE_TITLES: Final[MappingProxyType[str, str]] = _process_state_field_titles()


def query_all_process_states() -> Dict[int, ProcessState]:
    result = dict()
    for proc in psutil.process_iter():
        state = ProcessState.from_process(proc)
        if state.error is not None:
            continue
        result[proc.pid] = state
    return result
