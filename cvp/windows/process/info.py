# -*- coding: utf-8 -*-

import imgui

from cvp.imgui.button import button
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.process.process import Process
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.tab import TabItem


class ProcessInfoTab(TabItem[Process]):
    def __init__(self, context: RendererContext):
        super().__init__(context, "Info")

    @override
    def on_item(self, item: Process) -> None:
        imgui.text("Name:")
        input_text_disabled("## Name", item.name)

        imgui.text("PID:")
        input_text_disabled("## PID", str(item.pid))

        imgui.text("Status:")
        input_text_disabled("## Status", str(item.status()))

        imgui.separator()

        key = item.name
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
