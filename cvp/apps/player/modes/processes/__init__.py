# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui
from psutil import AccessDenied, NoSuchProcess, process_iter

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import MONITOR_EYE
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.table import BORDERS, ROW_BG
from cvp.types.override import override


class ProcessesMode(BaseMode):
    __cvp_mode_name__ = "Processes"
    __cvp_mode_icon__ = MONITOR_EYE

    _TABLE_COLUMNS: Final[int] = 4
    _TABLE_FLAGS: Final[int] = BORDERS | ROW_BG

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def config(self):
        return self.context.config.process

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                imgui.text("Process Monitoring")
                imgui.separator()
                self.on_child_process()

    def on_child_process(self) -> None:
        if imgui.begin_table("Table", self._TABLE_COLUMNS, self._TABLE_FLAGS):
            try:
                imgui.table_setup_column("PID")
                imgui.table_setup_column("Name")
                imgui.table_setup_column("Status")
                imgui.table_setup_column("Threads")
                imgui.table_headers_row()

                for proc in process_iter(("pid", "name", "status", "num_threads")):
                    try:
                        imgui.table_next_row()

                        imgui.table_set_column_index(0)
                        imgui.text(str(proc.pid))

                        imgui.table_set_column_index(1)
                        imgui.text(proc.name())

                        imgui.table_set_column_index(2)
                        imgui.text(proc.status())

                        imgui.table_set_column_index(3)
                        imgui.text(str(proc.num_threads()))
                    except (NoSuchProcess, AccessDenied):
                        continue
            finally:
                imgui.end_table()
