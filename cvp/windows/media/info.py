# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.config.sections.media import MediaWindowConfig
from cvp.ffmpeg.ffprobe.inspect import inspect_video_frame_size
from cvp.imgui.button import button
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.push_item_width import item_width
from cvp.logging.logging import logger
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.tab import TabItem


class MediaInfoTab(TabItem[MediaWindowConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(context, "Info")

    @override
    def on_item(self, item: MediaWindowConfig) -> None:
        imgui.text("Section:")
        input_text_disabled("## Section", item.uuid)

        imgui.text("Title:")
        with item_width(-1):
            item.title = input_text_value("## Title", item.title)

        imgui.text("File:")
        with item_width(-1):
            item.file = input_text_value("## File", item.file)

        spawnable = self.context.pm.spawnable(item.uuid)
        stoppable = self.context.pm.stoppable(item.uuid)
        removable = self.context.pm.removable(item.uuid)

        imgui.separator()
        imgui.text("Frame:")
        item.frame_size = imgui.input_int2("Size", *item.frame_size)[1]
        if imgui.button("Reset"):
            item.frame_size = 0, 0
        imgui.same_line()
        if imgui.button("Inspect"):
            try:
                item.frame_size = inspect_video_frame_size(item.file)
            except BaseException as e:
                logger.error(e)

        imgui.separator()
        status = self.context.pm.status(item.uuid)
        imgui.text(f"Process ({status})")

        if button("Spawn", disabled=not spawnable):
            self.context.pm.spawn_ffmpeg_with_file(
                key=item.uuid,
                file=item.file,
                width=item.frame_width,
                height=item.frame_height,
            )
        imgui.same_line()
        if button("Stop", disabled=not stoppable):
            self.context.pm.interrupt(item.uuid)
        imgui.same_line()
        if button("Remove", disabled=not removable):
            self.context.pm.pop(item.uuid)

        imgui.separator()
        imgui.text("Window visibility")
        if button("Show", disabled=item.opened):
            item.opened = True
        imgui.same_line()
        if button("Hide", disabled=not item.opened):
            item.opened = False
