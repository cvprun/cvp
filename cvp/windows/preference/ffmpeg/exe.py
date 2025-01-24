# -*- coding: utf-8 -*-

from shutil import which
from typing import List, Optional, Sequence

import imgui

from cvp.config.sections.proxies.ffmpeg import FFmpegProxy, FFprobeProxy
from cvp.imgui.button import button
from cvp.patterns.proxy import ValueProxy
from cvp.popups.open_file import OpenFilePopup
from cvp.renderer.context import RendererContext
from cvp.renderer.popup.base import PopupBase
from cvp.renderer.popup.propagator import PopupPropagator
from cvp.resources.download.links.ffmpeg import FFMPEG_LINKS, FFPROBE_LINKS, LinkMap
from cvp.resources.download.runner import DownloadRunner
from cvp.system.platform import SysMach, get_system_machine
from cvp.types.override import override
from cvp.widgets.tab import TabBar, TabItem


class ExeItem(TabItem, PopupPropagator):
    _runner: Optional[DownloadRunner]

    def __init__(
        self,
        context: RendererContext,
        name: str,
        proxy: ValueProxy,
        links: LinkMap,
    ):
        super().__init__(context, label=name)
        self._filename = name
        self._proxy = proxy
        self._downs = {sm: context.make_downloader(link) for sm, link in links.items()}

        self._sms = list(str(sm) for sm in SysMach)
        self._current_sm = get_system_machine()
        self._current_sm_index = self._sms.index(str(self._current_sm))
        self._sms_index = self._current_sm_index

        self._browser = OpenFilePopup(
            f"Select {self._filename} executable",
            target=self.on_browser,
        )
        self._runner = None

    @classmethod
    def from_ffmpeg(cls, context: RendererContext):
        return cls(
            context=context,
            name="ffmpeg",
            proxy=FFmpegProxy(context.config.ffmpeg),
            links=FFMPEG_LINKS,
        )

    @classmethod
    def from_ffprobe(cls, context: RendererContext):
        return cls(
            context=context,
            name="ffprobe",
            proxy=FFprobeProxy(context.config.ffmpeg),
            links=FFPROBE_LINKS,
        )

    @property
    @override
    def popups(self) -> Sequence[PopupBase]:
        return [self._browser]

    @property
    def exe_path(self) -> str:
        return self._proxy.get()

    @exe_path.setter
    def exe_path(self, value: str) -> None:
        self._proxy.set(value)

    def on_browser(self, file: str) -> None:
        self.exe_path = file

    @override
    def on_process(self) -> None:
        imgui.text(f"{self._label} executable")

        path_result = imgui.input_text(
            "##Path",
            self.exe_path,
            imgui.INPUT_TEXT_ENTER_RETURNS_TRUE,
        )

        path_changed = path_result[0]
        if path_changed:
            path_value = path_result[1]
            assert isinstance(path_value, str)
            self.exe_path = path_value

        if imgui.button("Default"):
            self.exe_path = self._filename

        imgui.same_line()
        which_path = which(self._filename)
        if button("Which", disabled=not which_path):
            assert isinstance(which_path, str)
            self.exe_path = which_path

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
            imgui.text_colored("This platform is not supported", 1.0, 0.1, 0.1)
            return

        if self._sms_index != self._current_sm_index:
            imgui.text_colored("Does not match the current platform", 1.0, 1.0, 0.0)

        imgui.text("URL:")
        imgui.text_unformatted(down.url)

        if button("Download Archive", disabled=self._runner is not None):
            self._runner = self.context.start_download_thread(down, 30.0, True)

        if self._runner is not None:
            imgui.text(str(self._runner.state))


class ExeTabs(TabBar, PopupPropagator):
    def __init__(self, context: RendererContext):
        super().__init__(context)
        self.register(ExeItem.from_ffmpeg(context))
        self.register(ExeItem.from_ffprobe(context))

    @property
    @override
    def popups(self) -> Sequence[PopupBase]:
        result: List[PopupBase] = list()
        for item in self._items.values():
            if not isinstance(item, PopupPropagator):
                continue
            result.extend(item.popups)
        return result
