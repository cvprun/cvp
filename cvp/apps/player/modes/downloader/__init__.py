# -*- coding: utf-8 -*-

import os
from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import CLOUD_DOWNLOAD
from cvp.context.context import Context
from cvp.download.item import DownloadItem
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.calc_input_text_with_button_size import calc_input_text_width
from cvp.imgui.checkbox import checkbox
from cvp.imgui.flags.child import AUTO_RESIZE_Y
from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE
from cvp.imgui.flags.table import BORDERS, ROW_BG
from cvp.imgui.input_float import input_float
from cvp.imgui.input_text import input_text
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.types.override import override


class DownloaderMode(BaseMode):
    __cvp_mode_name__ = "Downloader"
    __cvp_mode_icon__ = CLOUD_DOWNLOAD

    _TOP_CHILD_FLAGS: Final[int] = AUTO_RESIZE_Y
    _DOWNLOAD_BUTTON_LABEL: Final[str] = "Download"

    _TABLE_COLUMNS: Final[int] = 8
    _TABLE_FLAGS: Final[int] = BORDERS | ROW_BG

    def __init__(self, context: Context):
        super().__init__(context)
        self._input_url = str()
        self._input_checksum = str()
        self._dir_browser = OpenFilePopup(
            "Select Download Directory",
            mode=OpenFilePopup.SELECT_DIRECTORY,
            target=self.on_dir_selected,
        )

    @property
    def config(self):
        return self.context.config.downloader

    @property
    def manager(self):
        return self.context.downloader

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            self.do_child_process()

        self._dir_browser.on_process()

    def on_dir_selected(self, file: str) -> None:
        if not os.path.exists(file):
            self.context.toast_error(f"'{file}' does not exist")
            return

        if not os.path.isdir(file):
            self.context.toast_error(f"'{file}' is not a directory")
            return

        if not os.access(file, os.W_OK):
            self.context.toast_error(f"'{file}' is not writable")
            return

        self.config.download_dir = file

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
        input_text_width = calc_input_text_width(self._DOWNLOAD_BUTTON_LABEL)
        imgui.set_next_item_width(input_text_width)
        url_result = input_text("##URL", self._input_url, ENTER_RETURNS_TRUE)
        self._input_url = url_result.value

        imgui.same_line()

        download_clicked = button(
            self._DOWNLOAD_BUTTON_LABEL,
            disabled=not self._input_url,
        )
        if self._input_url and (url_result or download_clicked):
            self.context.downloader.add_download(self._input_url)
            self._input_url = str()

        if imgui.collapsing_header("Advanced options"):
            self.do_advanced_options()

    def do_advanced_options(self) -> None:
        if platform_dir := checkbox(
            "Use platform download directory",
            self.config.use_platform_download_dir,
        ):
            self.config.use_platform_download_dir = platform_dir.state

        imgui.begin_disabled(disabled=self.config.use_platform_download_dir)
        try:
            if down_dir := input_text("Download directory", self.config.download_dir):
                self.config.download_dir = down_dir.value
        finally:
            imgui.end_disabled()

        if button("Browse", disabled=self.config.use_platform_download_dir):
            self._dir_browser.show()
        imgui.same_line()
        if button("User Platform Dir", disabled=self.config.use_platform_download_dir):
            self.config.update_user_downloads_dir()

        if use_timeout := checkbox("Use timeout", self.config.use_timeout):
            self.config.use_timeout = use_timeout.state

        imgui.begin_disabled(disabled=not self.config.use_timeout)
        try:
            if timeout := input_float("Timeout", self.config.timeout):
                self.config.timeout = timeout.value
        finally:
            imgui.end_disabled()

        if redirects := checkbox("Follow Redirects", self.config.follow_redirects):
            self.config.follow_redirects = redirects.state

        if verify_ssl := checkbox("Verify SSL", self.config.verify_ssl):
            self.config.verify_ssl = verify_ssl.state

        if checksum := input_text("Checksum", self._input_checksum):
            self._input_checksum = checksum.value

        if button("Reset Default"):
            self.config.update_defaults()

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
