# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import CLOUD_DOWNLOAD
from cvp.context.context import Context
from cvp.download.item import DownloadItem
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
    __cvp_mode_icon__ = CLOUD_DOWNLOAD
    __cvp_mode_show__ = False

    _TOP_CHILD_FLAGS: Final[int] = AUTO_RESIZE_Y

    _TABLE_COLUMNS: Final[int] = 8
    _TABLE_FLAGS: Final[int] = BORDERS | ROW_BG

    def __init__(self, context: Context):
        super().__init__(context)
        self._download_label = "Download"
        self._input_url = str()

    @property
    def config(self):
        return self.context.config.downloader

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            self.do_child_process()

    def do_child_process(self) -> None:
        with begin_child_context("Top", child_flags=self._TOP_CHILD_FLAGS):
            self.do_top_process()

        imgui.separator()

        with begin_child_context("Table"):
            if imgui.begin_table("Download", self._TABLE_COLUMNS, self._TABLE_FLAGS):
                try:
                    imgui.table_setup_column("State")
                    imgui.table_setup_column("URL")
                    imgui.table_setup_column("Content-Length")
                    imgui.table_setup_column("Download")
                    imgui.table_setup_column("Progress")
                    imgui.table_setup_column("Speed")
                    imgui.table_setup_column("Elapsed")
                    imgui.table_setup_column("ETA")
                    imgui.table_headers_row()

                    for uuid, item in self.context.downloader.items():
                        imgui.table_next_row()
                        self.table_download_item_row(item)
                finally:
                    imgui.end_table()

    def do_top_process(self) -> None:
        input_text_width = calc_input_text_width(self._download_label)
        imgui.set_next_item_width(input_text_width)
        url_result = input_text("##URL", self._input_url, ENTER_RETURNS_TRUE)
        self._input_url = url_result.value

        imgui.same_line()

        download_clicked = button(self._download_label, disabled=not self._input_url)
        if self._input_url and (url_result or download_clicked):
            self.context.downloader.add_download(self._input_url)
            self._input_url = str()

        if imgui.collapsing_header("Advanced options"):
            pass

    @staticmethod
    def table_download_item_row(item: DownloadItem) -> None:
        imgui.table_set_column_index(0)
        imgui.text(item.state)

        imgui.table_set_column_index(1)
        imgui.text(item.url)

        imgui.table_set_column_index(2)
        imgui.text(str(item.content_length))

        imgui.table_set_column_index(3)
        imgui.text(str(item.download_length))

        imgui.table_set_column_index(4)
        imgui.text(f"{item.progress:%}")

        imgui.table_set_column_index(5)
        imgui.text(f"{item.speed_bps:.03f}")

        imgui.table_set_column_index(6)
        imgui.text(f"{item.elapsed:.03f}s")

        imgui.table_set_column_index(7)
        imgui.text(f"{item.eta:.03f}s")
