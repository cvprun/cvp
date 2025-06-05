# -*- coding: utf-8 -*-

from typing import Optional, Union

import psutil
from imgui_bundle import imgui

from cvp.context.context import Context
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.psutil.process.state import ProcessState
from cvp.psutil.process.updater import ProcessStateUpdater
from cvp.service.item import ServiceItem, ServiceKey


class ServicesStatusTab:
    _error: Optional[Union[BaseException, str]]

    def __init__(self, context: Context):
        self._context = context
        self._updater = ProcessStateUpdater(interval=1.0)
        self._error = None

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

    def get_process_state(self, key: ServiceKey) -> ProcessState:
        try:
            process_pid = self.services.get_process_pid(key)
            result = self._updater.update_pid(process_pid)
            self._error = None
            return result
        except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
            self._error = e
            return ProcessState()

    def __call__(self, service: ServiceItem) -> None:
        imgui.text("Process Status Browser")
        imgui.separator()

        stoppable = self.services.stoppable(service.key)
        imgui.begin_disabled(not stoppable)
        try:
            state = self.get_process_state(service.key)
            self.do_state_process(state)
        finally:
            imgui.end_disabled()

    def do_state_process(self, proc: ProcessState) -> None:
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
