# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.process._base import BaseProcessTab
from cvp.context.context import Context
from cvp.imgui.button import button
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.process.process import Process
from cvp.types.override import override


class ProcessInfoTab(BaseProcessTab):
    __cvp_process_tab_name__ = "Info"

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def do_process(self, process: Process) -> None:
        imgui.text("Name:")
        input_text_disabled("## Name", process.name)

        imgui.text("PID:")
        input_text_disabled("## PID", str(process.pid))

        imgui.text("Status:")
        input_text_disabled("## Status", str(process.status()))

        imgui.separator()

        key = process.name
        spawnable = self.context.pm.spawnable(key)
        stoppable = self.context.pm.stoppable(key)
        removable = self.context.pm.removable(key)

        if button("Spawn", disabled=not spawnable):
            pass
        imgui.same_line()
        if button("Stop", disabled=not stoppable):
            self.context.pm.interrupt(key)
        imgui.same_line()
        if button("Remove", disabled=not removable):
            self.context.pm.pop(key)
