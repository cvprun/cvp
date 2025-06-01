# -*- coding: utf-8 -*-

from datetime import datetime

import psutil
from imgui_bundle import imgui

from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import AUTO_RESIZE_Y, BORDERS
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.text_centered import text_centered
from cvp.imgui.widgets.table_mutable_mapping import table_mutable_mapping
from cvp.service.item import ServiceItem


class ServicesStatusTab:
    def __init__(self, context: Context):
        self._context = context

    @property
    def context(self):
        return self._context

    @property
    def services(self):
        return self.context.services

    def __call__(self, service: ServiceItem) -> None:
        process = self.services.get_process(service.key)
        if process is None:
            text_centered("No such process exists")
            return

        stoppable = self.services.stoppable(service.key)
        imgui.begin_disabled(not stoppable)
        try:
            self.do_psutil_process(process.psutil)
        finally:
            imgui.end_disabled()

    @staticmethod
    def do_psutil_process(proc: psutil.Process) -> None:
        input_text_disabled("PID", str(proc.pid))

        # input_text_disabled("Name", str(proc.name()))
        # input_text_disabled("Executable path", str(proc.exe()))
        # input_text_disabled("Command line", str(proc.cmdline()))

        try:
            envs = proc.environ()
        except psutil.NoSuchProcess:
            envs = dict()

        with begin_child_context(
            label="EnvChild",
            size=(imgui.calc_item_width(), 0),
            child_flags=AUTO_RESIZE_Y | BORDERS,
        ):
            table_mutable_mapping(
                label="EnvTable",
                container=envs,
                removable=False,
                show_key=True,
                show_value=True,
            )
        imgui.same_line(spacing=imgui.get_style().item_inner_spacing.x)
        imgui.text("Environment variables")

        create_time = datetime.fromtimestamp(proc.create_time()).isoformat()
        input_text_disabled("Create time", create_time)

        # input_text_disabled("Status", proc.status())
        # input_text_disabled("CWD", proc.cwd())
        # input_text_disabled("UIDs", str(proc.uids()))
        # input_text_disabled("GIDs", str(proc.gids()))
        # input_text_disabled("Terminal", str(proc.terminal()))
        # input_text_disabled("Nice", str(proc.nice()))
        # input_text_disabled("I/O niceness", str(proc.ionice()))
        # input_text_disabled("I/O counters", str(proc.io_counters()))
        # input_text_disabled("Context switches", str(proc.num_ctx_switches()))
