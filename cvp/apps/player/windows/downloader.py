# -*- coding: utf-8 -*-

from shutil import which
from typing import Mapping, Optional

from imgui_bundle import imgui

from cvp.context.context import Context
from cvp.imgui.button import button
from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.text_colored import text_colored
from cvp.patterns.proxy import ValueProxy
from cvp.resources.download.links.tuples import LinkInfo
from cvp.resources.download.runner import DownloadRunner
from cvp.system.platform import SysMach, get_system_machine


class ExecutableDownloader:
    def __init__(
        self,
        context: Context,
        filename: str,
        proxy: ValueProxy,
        links: Mapping[SysMach, LinkInfo],
        *,
        runner: Optional[DownloadRunner] = None,
    ):
        self._context = context
        self._filename = filename
        self._proxy = proxy
        self._downs = {sm: context.make_downloader(link) for sm, link in links.items()}

        self._sms = list(str(sm) for sm in SysMach)
        self._current_sm = get_system_machine()
        self._current_sm_index = self._sms.index(str(self._current_sm))
        self._sms_index = self._current_sm_index

        self._browser = OpenFilePopup(
            f"Select {self._filename} executable",
            target=self._on_browser,
        )
        self._runner = runner

    @property
    def filename(self):
        return self._filename

    @property
    def runner(self):
        return self._runner

    @property
    def browser(self):
        return self._browser

    @property
    def value(self) -> str:
        return self._proxy.get()

    @value.setter
    def value(self, value: str) -> None:
        self._proxy.set(value)

    def _on_browser(self, file: str) -> None:
        self.value = file

    def do_child_process(self) -> None:
        imgui.text(f"{self._filename} executable")

        path_result = imgui.input_text(
            "##Path",
            self.value,
            ENTER_RETURNS_TRUE,
        )

        path_changed = path_result[0]
        if path_changed:
            path_value = path_result[1]
            assert isinstance(path_value, str)
            self.value = path_value

        if imgui.button("Default"):
            self.value = self._filename

        imgui.same_line()
        which_path = which(self._filename)
        if button("Which", disabled=not which_path):
            assert isinstance(which_path, str)
            self.value = which_path

        imgui.same_line()
        if button("Cache"):
            pass

        imgui.same_line()
        if button("Browse"):
            self._browser.show()

        imgui.separator()

        imgui.text("Download statically compiled executables")

        self._sms_index = imgui.combo("##SysMach", self._sms_index, self._sms)[1]
        sys_mach = SysMach(self._sms[self._sms_index])

        if imgui.button("Check current platform"):
            self._sms_index = self._current_sm_index

        down = self._downs.get(sys_mach)
        if down is None:
            text_colored("This platform is not supported", (1.0, 0.1, 0.1, 1.0))
            return

        if self._sms_index != self._current_sm_index:
            text_colored("Does not match the current platform", (1.0, 1.0, 0.0, 1.0))

        imgui.text("URL:")
        imgui.text_unformatted(down.url)

        if button("Download Archive", disabled=self._runner is not None):
            self._runner = self._context.start_download_thread(down, 30.0, True)

        if self._runner is not None:
            imgui.text(str(self._runner.state))
