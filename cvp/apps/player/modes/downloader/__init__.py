# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.calc_input_text_with_button_size import calc_input_text_width
from cvp.imgui.flags.child import AUTO_RESIZE_Y
from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE
from cvp.imgui.flags.table import BORDERS, ROW_BG
from cvp.imgui.input_text import input_text
from cvp.types.override import override


class DownloaderMode(BaseMode):
    __cvp_mode_name__ = "Downloader"

    def __init__(self, context: Context):
        super().__init__(context)
        self._temp_url = str()
        self._download_button_label = "Download"

    @override
    def do_process(self) -> None:
        with self.begin_mode_context():
            self.do_child_process()

    def do_child_process(
        self,
        top_child_flags=AUTO_RESIZE_Y,
    ) -> None:
        with begin_child_context("TopBar", child_flags=top_child_flags):
            input_text_width = calc_input_text_width(self._download_button_label)
            imgui.set_next_item_width(input_text_width)
            url_result = input_text("##URL", self._temp_url, ENTER_RETURNS_TRUE)
            self._temp_url = url_result.value

            imgui.same_line()
            download_clicked = button("Download", disabled=not self._temp_url)
            if self._temp_url and (url_result or download_clicked):
                self.context.downloader.add_download(self._temp_url)
                self._temp_url = str()

        imgui.separator()

        with begin_child_context("Table"):
            if imgui.begin_table("Download", 7, BORDERS | ROW_BG):
                try:
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

                        imgui.table_set_column_index(1)
                        imgui.text(str(item.size))

                        imgui.table_set_column_index(2)
                        imgui.text(str(item.downloaded))

                        imgui.table_set_column_index(3)
                        imgui.text(str(item.state))

                        imgui.table_set_column_index(4)
                        imgui.text(str(item.progress))

                        imgui.table_set_column_index(5)
                        imgui.text(str(item.speed))

                        imgui.table_set_column_index(6)
                        imgui.text(str(item.eta))
                finally:
                    imgui.end_table()
