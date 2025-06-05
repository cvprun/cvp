# -*- coding: utf-8 -*-

from typing import Dict, Optional

from overrides import override
from psutil import AccessDenied, NoSuchProcess, process_iter

from cvp.psutil.process.state import ProcessState
from cvp.values.interval import IntervalUpdater


def query_all_process_infos() -> Dict[int, ProcessState]:
    result = dict()
    for proc in process_iter():
        try:
            result[proc.pid] = ProcessState.from_process(proc)
        except (AccessDenied, NoSuchProcess):
            continue
    return result


class Top(IntervalUpdater[Dict[int, ProcessState]]):
    def __init__(self, interval: Optional[float] = None):
        super().__init__(initial=query_all_process_infos(), interval=interval)

    @override
    def on_update(self) -> Dict[int, ProcessState]:
        return query_all_process_infos()
