# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.vms.medias._base import BaseMediaTab
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child, end_child
from cvp.imgui.flags.child import BORDERS
from cvp.imgui.text_centered import text_centered
from cvp.media.config import MediaConfig
from cvp.types.override import override


class MediaStreamTab(BaseMediaTab):
    __cvp_media_tab_name__ = "Stream"

    def __init__(self, context: Context):
        super().__init__(context)
        self._auto_scroll = True

    @override
    def do_process(self, media: MediaConfig) -> None:
        process = self.context.medias.get_process(media.key)
        if process is None:
            text_centered("Not found media process")
            return

        buffer = process.stderr_buffer
        if buffer is None:
            text_centered("The stream buffer does not exist")
            return

        buffer.update_safe()

        self._auto_scroll = imgui.checkbox("Auto Scroll", self._auto_scroll)[1]

        if begin_child("## Logging", child_flags=BORDERS):
            try:
                imgui.text_unformatted(buffer.getvalue())

                if self._auto_scroll:
                    # if imgui.get_scroll_y() >= imgui.get_scroll_max_y()
                    imgui.set_scroll_here_y(1.0)
            finally:
                end_child()
