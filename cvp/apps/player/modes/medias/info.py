# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.medias._base import BaseMediaTab
from cvp.context.context import Context
from cvp.ffmpeg.ffprobe.inspect import inspect_video_frame_size
from cvp.imgui.button import button
from cvp.imgui.input_int2 import input_int2
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_value import input_text_value
from cvp.logging.logging import logger
from cvp.media.config import MediaConfig
from cvp.types.override import override


class MediaInfoTab(BaseMediaTab):
    __cvp_media_tab_name__ = "Info"

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def do_process(self, media: MediaConfig) -> None:
        input_text_disabled("UUID", media.uuid)

        media.name = input_text_value("Name", media.name)
        media.file = input_text_value("File", media.file)

        spawnable = self.context.medias.spawnable(media.uuid)
        stoppable = self.context.medias.stoppable(media.uuid)
        removable = self.context.medias.removable(media.uuid)

        imgui.separator()
        if frame_size_result := input_int2(
            "Frame Size",
            media.frame_size[0],
            media.frame_size[1],
        ):
            media.frame_size = frame_size_result.value
        if imgui.button("Reset"):
            media.frame_size = 0, 0

        imgui.same_line()
        if imgui.button("Inspect"):
            try:
                media.frame_size = inspect_video_frame_size(media.file)
            except BaseException as e:
                logger.error(e)

        imgui.separator()
        status = self.context.medias.status(media.uuid)
        imgui.text(f"Process ({status})")

        if button("Spawn", disabled=not spawnable):
            self.context.medias.spawn_ffmpeg_with_file(
                key=media.uuid,
                file=media.file,
                width=media.frame_width,
                height=media.frame_height,
            )
        imgui.same_line()
        if button("Stop", disabled=not stoppable):
            self.context.medias.interrupt(media.uuid)
        imgui.same_line()
        if button("Remove", disabled=not removable):
            self.context.medias.removable_pop(media.uuid)

        imgui.separator()
        imgui.text("Window visibility")
        if button("Show", disabled=media.opened):
            media.opened = True
        imgui.same_line()
        if button("Hide", disabled=not media.opened):
            media.opened = False
