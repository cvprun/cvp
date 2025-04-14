# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.apps.player.windows.downloader import ExecutableDownloader
from cvp.config.sections.proxies.ffmpeg import FFmpegProxy, FFprobeProxy
from cvp.context.context import Context
from cvp.resources.download.links.ffmpeg import FFMPEG_LINKS, FFPROBE_LINKS
from cvp.types.override import override


class DownloaderPreference(BasePreference):
    __cvp_menu_name__ = "Downloader"

    def __init__(self, context: Context):
        super().__init__(context)
        ffmpeg = ExecutableDownloader(
            context=context,
            filename="ffmpeg",
            proxy=FFmpegProxy(context.config.ffmpeg),
            links=FFMPEG_LINKS,
        )
        ffprobe = ExecutableDownloader(
            context=context,
            filename="ffprobe",
            proxy=FFprobeProxy(context.config.ffmpeg),
            links=FFPROBE_LINKS,
        )

        self._downloaders = {
            "FFmpeg": ffmpeg,
            "FFprobe": ffprobe,
        }

    @override
    def do_process(self) -> None:
        if imgui.begin_tab_bar("DownloadTabBar"):
            try:
                for label, downloader in self._downloaders.items():
                    if imgui.begin_tab_item(label)[0]:
                        try:
                            downloader.do_child_process()
                        finally:
                            imgui.end_tab_item()
            finally:
                imgui.end_tab_bar()

    @override
    def do_postprocess(self) -> None:
        for downloader in self._downloaders.values():
            downloader.browser.do_process()
