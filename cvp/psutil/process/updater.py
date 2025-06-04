# -*- coding: utf-8 -*-

from typing import Dict, Optional

from overrides import override
from psutil import AccessDenied, NoSuchProcess, process_iter

from cvp.patterns.interval import IntervalUpdater
from cvp.psutil.process.info import ProcessInfo


def query_all_process_infos() -> Dict[int, ProcessInfo]:
    result = dict()
    for proc in process_iter():
        try:
            result[proc.pid] = ProcessInfo.from_process(proc)
        except (AccessDenied, NoSuchProcess):
            continue
    return result


class ProcessInfoUpdater(IntervalUpdater[ProcessInfo]):
    def __init__(self, pid: int, interval: Optional[float] = None):
        super().__init__(initial=ProcessInfo.from_pid(pid), interval=interval)
        self._pid = pid

    @override
    def on_update(self) -> ProcessInfo:
        return ProcessInfo.from_pid(self._pid)


class ProcessInfoDictUpdater(IntervalUpdater[Dict[int, ProcessInfo]]):
    def __init__(self, interval: Optional[float] = None):
        super().__init__(initial=query_all_process_infos(), interval=interval)

    @override
    def on_update(self) -> Dict[int, ProcessInfo]:
        return query_all_process_infos()
