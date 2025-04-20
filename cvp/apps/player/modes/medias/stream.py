# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

from imgui_bundle import imgui

from cvp.apps.player.modes.medias._base import BaseMediaTab
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child, end_child
from cvp.imgui.flags.child import BORDERS
from cvp.imgui.text_centered import text_centered
from cvp.media.config import MediaConfig
from cvp.types.override import override


@unique
class StreamType(StrEnum):
    both = auto()
    stdout = auto()
    stderr = auto()


class MediaStreamTab(BaseMediaTab):
    __cvp_media_tab_name__ = "Stream"

    def __init__(self, context: Context):
        super().__init__(context)
        self._stream = StreamType.stdout
        self._auto_scroll = True

    @override
    def do_process(self, media: MediaConfig) -> None:
        if imgui.radio_button("Both", self._stream == StreamType.both):
            self._stream = StreamType.both
        imgui.same_line()
        if imgui.radio_button("Stdout", self._stream == StreamType.stdout):
            self._stream = StreamType.stdout
        imgui.same_line()
        if imgui.radio_button("Stderr", self._stream == StreamType.stderr):
            self._stream = StreamType.stderr

        imgui.separator()

        process = self.context.medias.get_process(media.uuid)
        if process is None:
            text_centered("Not found media process")
            return

        match self._stream:
            case StreamType.stdout:
                buffer = process.stdout_buffer
            case StreamType.stderr:
                buffer = process.stderr_buffer
            case _:
                assert False, "Inaccessible section"

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
