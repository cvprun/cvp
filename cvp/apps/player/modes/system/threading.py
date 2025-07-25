# -*- coding: utf-8 -*-

import threading
from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes.system._base import BaseSystem
from cvp.assets.fonts.mdi import MULTICAST
from cvp.context.context import Context
from cvp.imgui.flags.table import BORDERS, ROW_BG
from cvp.types.override import override


class ThreadingSystem(BaseSystem):
    __cvp_menu_name__ = "Threading"
    __cvp_menu_icon__ = MULTICAST

    _TABLE_COLUMNS: Final[int] = 4
    _TABLE_FLAGS: Final[int] = BORDERS | ROW_BG

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def on_process(self) -> None:
        imgui.text("Thread Monitoring")
        imgui.separator()
        self.do_child_process()

    def do_child_process(self) -> None:
        if imgui.begin_table("Table", self._TABLE_COLUMNS, self._TABLE_FLAGS):
            try:
                imgui.table_setup_column("Identifier")
                imgui.table_setup_column("Name")
                imgui.table_setup_column("Alive")
                imgui.table_setup_column("Daemon")
                imgui.table_headers_row()

                for thread in threading.enumerate():
                    imgui.table_next_row()

                    if thread.ident is not None:
                        imgui.table_set_column_index(0)
                        imgui.text(str(thread.ident))

                    imgui.table_set_column_index(1)
                    imgui.text(thread.name)

                    imgui.table_set_column_index(2)
                    imgui.text(str(thread.is_alive()))

                    imgui.table_set_column_index(3)
                    imgui.text(str(thread.daemon))
            finally:
                imgui.end_table()
