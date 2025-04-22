# -*- coding: utf-8 -*-
import os.path
from typing import Final, Optional

from imgui_bundle import imgui

from cvp.apps.player.modes.medias._base import BaseMediaTab
from cvp.context.context import Context
from cvp.ffmpeg.ffprobe.inspect import inspect_video_frame_size
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.flags.child import BORDERS, RESIZE_X, RESIZE_Y
from cvp.imgui.input_int2 import input_int2
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_value import input_text_value
from cvp.logging.logging import logger
from cvp.media.config import MediaConfig
from cvp.types.override import override

_PREVIEW_NAME: Final[str] = "Preview"
_PREVIEW_WIDTH: Final[int] = 400
_PREVIEW_HEIGHT: Final[int] = 300
_PREVIEW_CHILD_FLAGS: Final[int] = RESIZE_X | RESIZE_Y | BORDERS


class MediaInfoTab(BaseMediaTab):
    __cvp_media_tab_name__ = "Info"

    _inspect_media: Optional[MediaConfig]

    def __init__(self, context: Context):
        super().__init__(context)
        self._inspect_media = None
        self._inspect_runner = self.context.create_thread_runner(self._on_inspect)

    @property
    def timeout(self) -> float:
        return 5.0

    def _on_inspect(self, timeout: Optional[float] = None) -> None:
        assert self._inspect_media is not None
        ffprobe = self.context.config.ffmpeg.ffprobe
        if not os.path.isfile(ffprobe):
            raise ValueError(f"ffprobe is not exists: '{ffprobe}'")
        if not os.access(ffprobe, os.X_OK):
            raise PermissionError(f"ffprobe is not executable: '{ffprobe}'")
        try:
            self._inspect_media.frame_size = inspect_video_frame_size(
                self._inspect_media.file,
                timeout=timeout,
                ffprobe=ffprobe,
            )
        except BaseException as e:
            logger.error(e)

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

        inspect_running = self._inspect_runner.running

        imgui.same_line()
        if button("Inspect", disabled=inspect_running):
            self._inspect_media = media
            self._inspect_runner(self.timeout)

        imgui.separator()
        status = self.context.medias.status(media.uuid)
        imgui.text(f"Process ({status})")

        valid_frame_size = media.valid_frame_size
        disabled_spawn = not spawnable or inspect_running or not valid_frame_size
        if button("Spawn", disabled=disabled_spawn):
            self.context.medias.spawn_ffmpeg(
                key=media.uuid,
                file=media.file,
                width=media.frame_width,
                height=media.frame_height,
            )
        imgui.same_line()
        if button("Stop", disabled=not stoppable or inspect_running):
            self.context.medias.interrupt(media.uuid)
        imgui.same_line()
        if button("Remove", disabled=not removable or inspect_running):
            self.context.medias.removable_pop(media.uuid)

        imgui.separator()
        imgui.text("Window visibility")
        if button("Show", disabled=media.opened):
            media.opened = True
        imgui.same_line()
        if button("Hide", disabled=not media.opened):
            media.opened = False

        if not media.opened:
            return

        texture = self.medias.get_latest_texture(media.uuid)
        if not texture:
            return

        imgui.separator()
        self.do_preview_process(texture)

    @staticmethod
    def do_preview_process(
        texture: int,
        name=_PREVIEW_NAME,
        width=_PREVIEW_WIDTH,
        height=_PREVIEW_HEIGHT,
        child_flags=_PREVIEW_CHILD_FLAGS,
    ):
        with begin_child_context(name, width, height, child_flags=child_flags):
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
