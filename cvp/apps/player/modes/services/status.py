# -*- coding: utf-8 -*-

from typing import Optional, Union

import psutil
from imgui_bundle import imgui

from cvp.context.context import Context
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.patterns.delta import Delta
from cvp.patterns.interval import IntervalUpdater
from cvp.psutil.process.info import ProcessInfo
from cvp.service.item import ServiceItem, ServiceKey
from cvp.variables import UNKNOWN_PID


class ServicesStatusTab:
    _error: Optional[Union[BaseException, str]]
    _pid: Delta[int]
    _updater: IntervalUpdater[ProcessInfo]

    def __init__(self, context: Context):
        self._context = context
        self._error = None
        self._pid = Delta.from_single_value(UNKNOWN_PID)
        self._updater = IntervalUpdater(
            initial=ProcessInfo(),
            interval=1.0,
            updater=self.on_update_process_info,
        )

    @property
    def context(self):
        return self._context

    @property
    def services(self):
        return self.context.services

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    def text_error(self, text: str) -> None:
        imgui.text_colored(self.error_color, text)

    def on_update_process_info(self) -> ProcessInfo:
        if self._pid.value == UNKNOWN_PID:
            return ProcessInfo()
        else:
            return ProcessInfo.from_pid(self._pid.value)

    def get_latest_info(self, key: ServiceKey) -> ProcessInfo:
        pid = self.services.get_process_pid(key)

        try:
            if self._pid.update(pid):
                result = self._updater.force_update()
            else:
                result = self._updater.get()

            self._error = None
            return result
        except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
            self._error = e
            return ProcessInfo()

    def __call__(self, service: ServiceItem) -> None:
        imgui.text("Process Status Browser")
        imgui.separator()

        stoppable = self.services.stoppable(service.key)
        imgui.begin_disabled(not stoppable)
        try:
            self.do_psutil_process(self.get_latest_info(service.key))
        finally:
            imgui.end_disabled()

    def do_psutil_process(self, proc: ProcessInfo) -> None:
        if self._error is not None:
            self.text_error(str(self._error))

        input_text_disabled("PID", str(proc.pid))
        input_text_disabled("PPID", str(proc.ppid))
        input_text_disabled("Name", proc.name)
        input_text_disabled("Status", proc.status)
        input_text_disabled("Executable path", proc.exe)
        input_text_disabled("Command line", str(proc.cmdline))
        input_text_disabled("Create time", proc.create_time.isoformat())
        input_text_disabled("CWD", proc.cwd)
        # input_text_disabled("UIDs", str(proc.uids()))
        # input_text_disabled("GIDs", str(proc.gids()))
        # input_text_disabled("Terminal", str(proc.terminal()))
        input_text_disabled("Nice", str(proc.nice))
        # input_text_disabled("I/O niceness", str(proc.ionice()))
        # input_text_disabled("I/O counters", str(proc.io_counters()))
        # input_text_disabled("Context switches", str(proc.num_ctx_switches()))
        input_text_disabled("Username", proc.username)
