# -*- coding: utf-8 -*-

from ctypes import addressof, c_void_p, create_string_buffer, memmove

from imgui_bundle import imgui
from OpenGL import GL

from cvp.apps.player.modes.medias._base import BaseMediaTab
from cvp.context.context import Context
from cvp.imgui.canvas import canvas_context
from cvp.imgui.draw_list.types import DrawList
from cvp.media.config import MediaConfig
from cvp.types.override import override


class MediaPlayerTab(BaseMediaTab):
    __cvp_media_tab_name__ = "Player"

    def __init__(self, context: Context):
        super().__init__(context)
        self._clear_color = 0.5, 0.5, 0.5, 1.0
        self._texture = 0
        self._pbo = 0
        self._prev_frame_index = 0
        self._min_width = 800
        self._min_height = 600

    def create(self) -> None:
        assert self._texture == 0
        assert self._pbo == 0

        self._texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_RGB,
            self._min_width,
            self._min_height,
            0,
            GL.GL_RGB,
            GL.GL_UNSIGNED_BYTE,
            None,
        )
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

        self._pbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, self._pbo)
        size = self._min_width * self._min_height * 3
        GL.glBufferData(GL.GL_PIXEL_UNPACK_BUFFER, size, None, GL.GL_STREAM_DRAW)
        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, 0)

        assert self._texture != 0
        assert self._pbo != 0

    def destroy(self) -> None:
        assert self._texture != 0
        assert self._pbo != 0

        GL.glDeleteTextures(1, self._texture)
        self._texture = 0

        GL.glDeleteBuffers(1, self._pbo)
        self._pbo = 0

    @override
    def do_process(self, media: MediaConfig) -> None:
        with canvas_context(
            "Canvas",
            clear_color=self._clear_color,
            rect_filled=True,
        ) as draw_list:
            self.on_canvas(media, draw_list)

    def update_texture(self, media: MediaConfig) -> None:
        if not self._texture:
            return

        process = self.context.pm.get(media.uuid)
        if process is None:
            return

        if process.poll() is not None:
            return

        pixels = process.dequeue_latest()
        if not pixels:
            return

        if self._prev_frame_index == process.latest_count:
            return

        self._prev_frame_index = process.latest_count
        width = process.frame_shape.width
        height = process.frame_shape.height
        channels = process.frame_shape.channels

        if width <= 0 or height <= 0:
            return

        assert isinstance(width, int)
        assert isinstance(height, int)
        assert isinstance(channels, int)
        assert channels == 3

        self.update_texture_image_2d(width, height, pixels)
        # self.update_texture_with_pbo(width, height, channels, pixels)

    def update_texture_image_2d(self, width: int, height: int, pixels: bytes) -> None:
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_RGB,
            width,
            height,
            0,
            GL.GL_RGB,
            GL.GL_UNSIGNED_BYTE,
            pixels,
        )
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def update_texture_with_pbo(
        self,
        width: int,
        height: int,
        channels: int,
        pixels: bytes,
    ) -> None:
        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, self._pbo)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)
        GL.glTexSubImage2D(
            GL.GL_TEXTURE_2D,
            0,
            0,
            0,
            width,
            height,
            GL.GL_RGB,
            GL.GL_UNSIGNED_BYTE,
            c_void_p(0),
        )

        size = width * height * channels

        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, self._pbo)
        GL.glBufferData(GL.GL_PIXEL_UNPACK_BUFFER, size, None, GL.GL_STREAM_DRAW)

        buffer_ptr = GL.glMapBuffer(GL.GL_PIXEL_UNPACK_BUFFER, GL.GL_WRITE_ONLY)
        if buffer_ptr:
            pixels_ptr = addressof(create_string_buffer(pixels, size))
            memmove(buffer_ptr, pixels_ptr, size)
            GL.glUnmapBuffer(GL.GL_PIXEL_UNPACK_BUFFER)

        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, 0)

    def on_canvas(self, media: MediaConfig, draw_list: DrawList):
        self.update_texture(media)

        screen_pos = imgui.get_cursor_screen_pos()
        region_size = imgui.get_content_region_avail()
        cx = screen_pos.x
        cy = screen_pos.y
        cw = region_size.x
        ch = region_size.y

        p1 = cx, cy
        p2 = cx + cw, cy + ch
        draw_list.add_image(self._texture, p1, p2, (0, 0), (1, 1))
