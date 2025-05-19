# -*- coding: utf-8 -*-

from datetime import datetime

from imgui_bundle import imgui

from cvp.apps.player.modes.medias._base import BaseMediaTab
from cvp.context.context import Context
from cvp.ffmpeg.ffprobe.inspect import inspect_video_frame_size
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.flags.child import BORDERS, RESIZE_X, RESIZE_Y
from cvp.imgui.input_float import input_float
from cvp.imgui.input_int2 import input_int2
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.spinner import spinner
from cvp.logging.logging import logger
from cvp.media.config import MediaConfig
from cvp.types.override import override


class MediaInfoTab(BaseMediaTab):
    __cvp_media_tab_name__ = "Info"

    def __init__(self, context: Context):
        super().__init__(context)
        self._inspect_begin = datetime.now().astimezone()
        self._inspect_runner = self.context.create_thread_runner(self._on_inspect)

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    @staticmethod
    def _on_inspect(ffprobe: str, media: MediaConfig) -> None:
        try:
            media.frame_size = inspect_video_frame_size(
                media.file,
                timeout=media.inspect_timeout,
                ffprobe=ffprobe,
            )
        except BaseException as e:
            logger.error(e)
            raise

    def inspect_frame_size(self, media: MediaConfig) -> None:
        if self._inspect_runner.running:
            raise ValueError("Inspection is already running")

        try:
            self._inspect_runner(self.context.config.ffmpeg.ffprobe, media)
            self._inspect_begin = datetime.now().astimezone()
        except BaseException as e:
            logger.exception(e)
            self.context.toast(f"Inspection failed: '{e}'")

    @override
    def on_process(self, media: MediaConfig) -> None:
        input_text_disabled("UUID", media.key)

        media.name = input_text_value("Name", media.name)
        media.file = input_text_value("File", media.file)

        spawnable = self.context.medias.spawnable(media.key)
        stoppable = self.context.medias.stoppable(media.key)
        removable = self.context.medias.removable(media.key)

        if timeout := input_float("Inspect timeout", media.inspect_timeout, step=1.0):
            media.inspect_timeout = timeout.value

        imgui.separator()
        if frame_size_result := input_int2(
            "Frame Size",
            media.frame_size[0],
            media.frame_size[1],
        ):
            media.frame_size = frame_size_result.value
        if imgui.button("Reset default"):
            media.update_default_frame_size()

        inspect_running = self._inspect_runner.running

        imgui.same_line()
        if button("Inspect", disabled=inspect_running):
            self.inspect_frame_size(media)

        if inspect_running:
            imgui.same_line()
            spinner("Running Spinner")

            imgui.same_line()
            duration = datetime.now().astimezone() - self._inspect_begin
            remain_seconds = media.inspect_timeout - duration.total_seconds()
            imgui.text(f"{remain_seconds:.01f}s")

        if self._inspect_runner.error is not None:
            imgui.text_colored(self.error_color, str(self._inspect_runner.error))

        imgui.separator()
        status = self.context.medias.status(media.key)
        imgui.text(f"Process ({status})")

        valid_frame_size = media.valid_frame_size
        disabled_spawn = not spawnable or inspect_running or not valid_frame_size
        if button("Spawn", disabled=disabled_spawn):
            self.context.medias.spawn_ffmpeg(
                key=media.key,
                file=media.file,
                width=media.frame_width,
                height=media.frame_height,
            )
        imgui.same_line()
        if button("Stop", disabled=not stoppable or inspect_running):
            self.context.medias.interrupt(media.key)
        imgui.same_line()
        if button("Remove", disabled=not removable or inspect_running):
            self.context.medias.removable_pop(media.key)

        imgui.separator()
        imgui.text("Window visibility")
        if button("Show", disabled=media.opened):
            media.opened = True
        imgui.same_line()
        if button("Hide", disabled=not media.opened):
            media.opened = False

        if not media.opened:
            return

        texture = self.medias.get_latest_texture(media.key)
        if not texture:
            return

        imgui.separator()
        self.do_preview_process(texture)

    @staticmethod
    def do_preview_process(
        texture: int,
        width=400,
        height=300,
        child_flags=RESIZE_X | RESIZE_Y | BORDERS,
    ):
        with begin_child_context(
            label="Preview",
            size=(width, height),
            child_flags=child_flags,
        ):
            screen_pos = imgui.get_cursor_screen_pos()
            region_size = imgui.get_content_region_avail()

            cx = screen_pos.x
            cy = screen_pos.y
            cw = region_size.x
            ch = region_size.y

            p1 = cx, cy
            p2 = cx + cw, cy + ch

            draw_list = get_window_draw_list()
            draw_list.add_image(texture, p1, p2, (0, 0), (1, 1))
