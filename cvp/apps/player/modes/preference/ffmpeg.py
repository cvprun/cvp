# -*- coding: utf-8 -*-

import os
from shutil import which
from subprocess import check_output
from typing import Dict, Optional, Union

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.button import button
from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE
from cvp.imgui.input_text import input_text
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.spinner import spinner
from cvp.patterns.proxy import ValueProxy
from cvp.types.override import override


class FFmpegPreference(BasePreference):
    __cvp_menu_name__ = "FFmpeg"

    def __init__(
        self,
        context: Context,
        *,
        result: Optional[Dict[str, Union[str, BaseException]]] = None,
    ):
        super().__init__(context)
        self._executable_proxy: Optional[ValueProxy[str]] = None
        self._outputs = dict(result if result else {})
        self._version_runner = context.create_thread_runner(self._on_version_main)
        self._executable_browser = OpenFilePopup(
            "Select Executable File",
            target=self._on_file_selected,
        )

    def _on_version_main(self, filename: str, path: str) -> None:
        try:
            self._outputs[filename] = check_output([path, "-version"], encoding="utf-8")
        except BaseException as e:
            self._outputs[filename] = e

    def _on_file_selected(self, file: str) -> None:
        if not os.path.exists(file):
            self.context.toast_error(f"'{file}' does not exist")
            return

        if not os.path.isfile(file):
            self.context.toast_error(f"'{file}' is not a file")
            return

        if not os.access(file, os.X_OK):
            self.context.toast_error(f"'{file}' is not executable")
            return

        assert self._executable_proxy is not None
        try:
            self._executable_proxy.set(file)
        finally:
            self._executable_proxy = None

    def show_executable_browser(self, proxy: ValueProxy[str]) -> None:
        self._executable_proxy = proxy
        self._executable_browser.show()

    def text_error(self, text: str) -> None:
        imgui.text_colored(self.context.config.appearance.error_color, text)

    def text_warning(self, text: str) -> None:
        imgui.text_colored(self.context.config.appearance.warning_color, text)

    def text_success(self, text: str) -> None:
        imgui.text_colored(self.context.config.appearance.success_color, text)

    @override
    def do_process(self) -> None:
        if imgui.begin_tab_bar(type(self).__name__):
            try:
                self.do_executable_tab(
                    filename="ffmpeg",
                    proxy=self.context.config.ffmpeg.create_ffmpeg_proxy(),
                )
                self.do_executable_tab(
                    filename="ffprobe",
                    proxy=self.context.config.ffmpeg.create_ffprobe_proxy(),
                )
            finally:
                imgui.end_tab_bar()

    @override
    def do_postprocess(self) -> None:
        self._executable_browser.do_process()

    def do_executable_tab(self, filename: str, proxy: ValueProxy[str]) -> None:
        if imgui.begin_tab_item(filename)[0]:
            try:
                self.do_executable_process(filename, proxy)
            finally:
                imgui.end_tab_item()

    def do_executable_process(self, filename: str, proxy: ValueProxy[str]) -> None:
        imgui.text(f"The {filename} executable")

        if path_result := input_text("Path", proxy.get(), ENTER_RETURNS_TRUE):
            proxy.set(path_result.value)

        if proxy.get() == filename:
            self.text_warning("The default value is no validation")
        else:
            if not os.path.exists(proxy.get()):
                self.text_error("The specified path does not exist")
            elif not os.path.isfile(proxy.get()):
                self.text_error("The specified path is not a file")
            elif not os.access(proxy.get(), os.X_OK):
                self.text_error("The specified file is not executable")
            else:
                self.text_success("Valid executable file")

        if imgui.button("Default"):
            proxy.set(filename)
        imgui.same_line()
        imgui.text("Use only the filename")

        which_path = which(filename)
        if button("Which", disabled=not which_path):
            assert isinstance(which_path, str)
            proxy.set(which_path)
        imgui.same_line()
        imgui.text("Use the path found on the system")

        cache_path = str(self.context.home.bin / filename)
        if button("Cache"):
            proxy.set(cache_path)
        imgui.same_line()
        imgui.text("Uses the predefined application cache path")

        if button("Browse"):
            self.show_executable_browser(proxy)
        imgui.same_line()
        imgui.text("Find it yourself")

        imgui.separator()

        if button("Show version"):
            self._version_runner(filename, proxy.get())

        if self._version_runner.running:
            spinner("Running Spinner")
            return

        result = self._outputs.get(filename)
        if not result:
            return

        if isinstance(result, str):
            imgui.text_wrapped(result)
        elif isinstance(result, BaseException):
            self.text_error(str(result))
        else:
            assert False, "Inaccessible section"
