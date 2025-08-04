# -*- coding: utf-8 -*-

import os

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.button import button
from cvp.imgui.checkbox import checkbox
from cvp.imgui.input_float import input_float
from cvp.imgui.input_text import input_text
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.types.override import override


class DownloaderPreference(BasePreference):
    __cvp_menu_name__ = "Downloader"

    def __init__(self, context: Context):
        super().__init__(context)
        self._dir_browser = OpenFilePopup(
            "Select Download Directory",
            mode=OpenFilePopup.SELECT_DIRECTORY,
            target=self.on_dir_selected,
        )

    @property
    def config(self):
        return self.context.config.downloader

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

    @override
    def on_postprocess(self) -> None:
        self._dir_browser.on_process()

    @override
    def on_process(self) -> None:
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

        if button("Reset Default"):
            self.config.update_defaults()
