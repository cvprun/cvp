# -*- coding: utf-8 -*-

from typing import Dict, Optional

from overrides import override
from psutil import AccessDenied, NoSuchProcess, process_iter

from cvp.psutil.process.state import ProcessState
from cvp.values.delta import DeltaValue
from cvp.values.interval import IntervalUpdater
from cvp.variables import UNKNOWN_PID


class ProcessStateUpdater(IntervalUpdater[ProcessState]):
    pid: DeltaValue[int]

    def __init__(self, pid=UNKNOWN_PID, interval: Optional[float] = None):
        super().__init__(initial=ProcessState.from_pid(pid), interval=interval)
        self._pid = DeltaValue.from_single_value(pid)

    @override
    def on_update(self) -> ProcessState:
        return ProcessState.from_pid(self._pid)

    def update_pid(self, pid: int) -> ProcessState:
        try:
            if self._pid.update(pid):
                return self.force_update()
            else:
                return self.get()
        except:  # noqa
            result = ProcessState()
            self.set_result(result)
            return result


def query_all_process_infos() -> Dict[int, ProcessState]:
    result = dict()
    for proc in process_iter():
        try:
            result[proc.pid] = ProcessState.from_process(proc)
        except (AccessDenied, NoSuchProcess):
            continue
    return result


class ProcessInfoDictUpdater(IntervalUpdater[Dict[int, ProcessState]]):
    def __init__(self, interval: Optional[float] = None):
        super().__init__(initial=query_all_process_infos(), interval=interval)

    @override
    def on_update(self) -> Dict[int, ProcessState]:
        return query_all_process_infos()
