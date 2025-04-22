# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.context.context import Context
from cvp.imgui.flags.table import BORDERS, ROW_BG
from cvp.types.override import override


class DownloadMode(BaseMode):
    __cvp_mode_name__ = "Download"

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def do_process(self) -> None:
        with self.begin_mode_context():
            self.do_child_process()

    def do_child_process(self) -> None:
        if imgui.begin_table("Download", 7, BORDERS | ROW_BG):
            imgui.table_setup_column("URL")
            imgui.table_setup_column("Size")
            imgui.table_setup_column("Downloaded")
            imgui.table_setup_column("State")
            imgui.table_setup_column("Progress")
            imgui.table_setup_column("Speed")
            imgui.table_setup_column("ETA")
            imgui.table_headers_row()

            for uuid, item in self.context.downloader.items():
                imgui.table_next_row()

                imgui.table_set_column_index(0)
                imgui.text(item.url)

            imgui.end_table()
