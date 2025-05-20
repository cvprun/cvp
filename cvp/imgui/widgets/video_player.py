# -*- coding: utf-8 -*-

from typing import Optional

import mpv
from imgui_bundle import imgui

from cvp.gl.fbo.framebuffer import Framebuffer
from cvp.gl.runtime import get_opengl_process_address
from cvp.gl.textures.texture import Texture
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.draw_list.types import DrawList
from cvp.imgui.slider_float import slider_float
from cvp.logging.loggers import mpv_logger as logger
from cvp.logging.mpv import MpvLogLevel
from cvp.types.shapes_i import SizeI


class VideoPlayer:
    def __init__(self, file: str, size: SizeI, log_level=MpvLogLevel.debug):
        self._fbo = Framebuffer()
        self._fbo.open()

        with self._fbo:
            self._texture = Texture(size)
            self._fbo.attach_texture(self._texture.texture_id)

        self._playback_percentage = 0.0
        self._volume = 0.0

        self._log_level = log_level
        self._mpv = mpv.MPV(log_handler=self.on_log_handler, loglevel=log_level)

        get_proc_address = mpv.MpvGlGetProcAddressFn(self._get_process_address)
        opengl_init_params = {"get_proc_address": get_proc_address}
        self._render = mpv.MpvRenderContext(
            mpv=self._mpv,
            api_type="opengl",
            opengl_init_params=opengl_init_params,
        )

        self._mpv.play(file)
        self._mpv.volume = 0

    @staticmethod
    def _get_process_address(_, name):
        return get_opengl_process_address(str(name, encoding="utf-8"))

    def on_log_handler(self, level: int, prefix: str, text: str) -> None:
        logger.info(f"{self._log_level} {level} {prefix} {text}")

    def close(self) -> None:
        self._render.free()
        self._mpv.terminate()
        self._texture.close()
        self._fbo.close()

    @property
    def filename(self) -> str:
        return self._mpv.filename

    @property
    def time_pos(self) -> float:
        return self._mpv.time_pos

    @property
    def duration(self) -> float:
        return self._mpv.duration

    @property
    def playtime_remaining(self) -> float:
        return self._mpv.playtime_remaining

    def as_time_info(self) -> str:
        time_pos = self._mpv.time_pos
        duration = self._mpv.duration
        playtime_remaining = self._mpv.playtime_remaining

        assert isinstance(time_pos, float)
        assert isinstance(duration, float)
        assert isinstance(playtime_remaining, float)

        return f"{time_pos:.02f}s/{duration:.02f}s ({playtime_remaining:.02f}s)"

    def do_playback_slider(self, label: str):
        if result := slider_float(
            label=label,
            value=self._playback_percentage,
            min_value=0.0,
            max_value=100.0,
            fmt="Playback Percentage %.0f",
        ):
            try:
                self._mpv.command("seek", result.value, "absolute-percent")
            except:  # noqa
                pass
            self._playback_percentage = result.value
        elif self._mpv.percent_pos:
            self._playback_percentage = self._mpv.percent_pos

    def do_volume_slider(self, label: str):
        if result := slider_float(
            label=label,
            value=self._volume,
            min_value=0.0,
            max_value=100.0,
            fmt="Volume %.0f",
        ):
            self._mpv.volume = result.value
            self._volume = result.value
        elif self._mpv.volume:
            self._volume = self._mpv.volume

    def do_process(self, draw_list: Optional[DrawList] = None) -> None:
        if draw_list is None:
            draw_list = get_window_draw_list()
        assert draw_list is not None

        screen_pos = imgui.get_cursor_screen_pos()
        region_size = imgui.get_content_region_avail()

        cx, cy = screen_pos.x, screen_pos.y
        cw, ch = region_size.x, region_size.y

        image_min = cx, cy
        image_max = cx + cw, cy + ch

        if self._render.update() and 0 < cw and 0 < ch:
            video_width = int(cw)
            video_height = int(ch)

            with self._fbo:
                with self._texture:
                    self._texture.resize(video_width, video_height)

            fbo = self._fbo.framebuffer_id
            opengl_fbo = {"w": video_width, "h": video_height, "fbo": fbo}
            self._render.render(flip_y=False, opengl_fbo=opengl_fbo)

        draw_list.add_image(self._texture.texture_id, image_min, image_max)
        imgui.dummy(region_size)
