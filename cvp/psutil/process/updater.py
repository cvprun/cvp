# -*- coding: utf-8 -*-

from typing import Optional

from overrides import override

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
