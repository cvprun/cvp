# -*- coding: utf-8 -*-

from typing import List

import psutil

from cvp.patterns.delta import Delta
from cvp.patterns.temp import TempValue
from cvp.psutil.process.rlimit import ResourceLimits
from cvp.variables import DEFAULT_NICE, UNKNOWN_PID


class ServicesControlCache:
    pid: Delta[int]
    nice: TempValue[int]
    ionice_class: TempValue[int]
    ionice_level: TempValue[int]
    cpu_affinity: TempValue[List[int]]
    rlimit: TempValue[ResourceLimits]

    def __init__(self):
        self.pid = Delta.from_single_value(UNKNOWN_PID)
        self.nice = TempValue.from_single_value(DEFAULT_NICE)
        self.ionice_class = TempValue.from_single_value(0)
        self.ionice_level = TempValue.from_single_value(0)
        self.cpu_indexes = list(range(psutil.cpu_count()))
        self.cpu_affinity = TempValue.from_single_value(list())
        self.rlimit = TempValue.from_single_value(ResourceLimits())

    def _update_nice(self, process: psutil.Process) -> None:
        self.nice.fill(process.nice())

    def _update_ionice(self, process: psutil.Process) -> None:
        if psutil.WINDOWS:
            # noinspection PyProtectedMember
            from psutil._pswindows import IOPriority

            windows_ionice = process.ionice()
            assert isinstance(windows_ionice, IOPriority)
            self.ionice_class.fill(int(windows_ionice))
            self.ionice_level.fill(0)
        elif psutil.LINUX:
            # noinspection PyProtectedMember
            from psutil._common import pionice

            linux_ionice = process.ionice()
            assert isinstance(linux_ionice, pionice)
            self.ionice_class.fill(linux_ionice.ioclass)
            self.ionice_level.fill(linux_ionice.value)
        else:
            self.ionice_class.fill(0)
            self.ionice_level.fill(0)

    def _update_cpu_affinity(self, process: psutil.Process) -> None:
        cpu_affinity = list(process.cpu_affinity() or ())
        self.cpu_affinity.fill(cpu_affinity, use_deepcopy=True)

    def _update_rlimit(self, process: psutil.Process) -> None:
        self.rlimit.fill(ResourceLimits.from_process(process), use_deepcopy=True)

    def force_update(self, process: psutil.Process) -> None:
        self._update_nice(process)
        self._update_ionice(process)
        self._update_cpu_affinity(process)
        self._update_rlimit(process)

    def update_if_pid_changed(self, process: psutil.Process) -> None:
        if not self.pid.update(process.pid):
            return

        self.force_update(process)
