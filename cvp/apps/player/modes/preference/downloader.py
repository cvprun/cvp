# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.button import button
from cvp.imgui.checkbox import checkbox
from cvp.imgui.combo_enum import combo_enum
from cvp.imgui.input_float import input_float
from cvp.imgui.input_text import input_text
from cvp.types.override import override


class DownloaderPreference(BasePreference):
    __cvp_menu_name__ = "Downloader"

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def config(self):
        return self.context.config.downloader

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

        if use_timeout := checkbox("Use timeout", self.config.use_timeout):
            self.config.use_timeout = use_timeout.state

        imgui.begin_disabled(disabled=not self.config.use_timeout)
        try:
            if timeout := input_float("Timeout", self.config.timeout):
                self.config.timeout = timeout.value
        finally:
            imgui.end_disabled()

        if checksum := combo_enum("Checksum Hash", self.config.checksum_hash):
            assert checksum.item is not None
            self.config.checksum = checksum.item

        if redirects := checkbox("Follow Redirects", self.config.follow_redirects):
            self.config.follow_redirects = redirects.state

        if verify_ssl := checkbox("Verify SSL", self.config.verify_ssl):
            self.config.verify_ssl = verify_ssl.state

        if button("Reset Default"):
            self.config.update_defaults()
