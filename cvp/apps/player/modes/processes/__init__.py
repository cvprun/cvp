# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import MONITOR_EYE
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.table import BORDERS, ROW_BG
from cvp.psutil.process import ProcessInfos, get_process_info_field_titles
from cvp.types.override import override


class ProcessesMode(BaseMode):
    __cvp_mode_name__ = "Processes"
    __cvp_mode_icon__ = MONITOR_EYE

    _TABLE_FLAGS: Final[int] = BORDERS | ROW_BG

    def __init__(self, context: Context):
        super().__init__(context)
        self._infos = ProcessInfos(interval=1.0)
        self._headers = get_process_info_field_titles()

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
        if imgui.begin_table("Table", len(self._headers), self._TABLE_FLAGS):
            try:
                for header in self._headers.values():
                    imgui.table_setup_column(header)
                imgui.table_headers_row()

                for proc in self._infos.get():
                    imgui.table_next_row()
                    for i, key in enumerate(self._headers.keys()):
                        imgui.table_set_column_index(i)
                        imgui.text(str(getattr(proc, key)))
            finally:
                imgui.end_table()
