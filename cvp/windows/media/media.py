# -*- coding: utf-8 -*-

from ctypes import addressof, c_void_p, create_string_buffer, memmove
from typing import Final, Tuple

from imgui_bundle import imgui
from OpenGL import GL

from cvp.config.sections.media import MediaWindowConfig
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.flags.window import NO_MOVE
from cvp.imgui.menu_item_ex import menu_item
from cvp.renderer.context import RendererContext
from cvp.renderer.window.base import WindowBase
from cvp.types.override import override

_WINDOW_NO_MOVE: Final[int] = imgui.WINDOW_NO_MOVE
_WINDOW_NO_SCROLLBAR: Final[int] = imgui.WINDOW_NO_SCROLLBAR
_WINDOW_NO_RESIZE: Final[int] = imgui.WINDOW_NO_RESIZE


class MediaWindow(WindowBase[MediaWindowConfig]):
    def __init__(self, context: RendererContext, window_config: MediaWindowConfig):
        super().__init__(
            context=context,
            window_config=window_config,
            title="Media",
            closable=True,
            flags=None,
            modifiable_title=True,
        )

        self._clear_color = 0.5, 0.5, 0.5, 1.0
        self._texture = 0
        self._pbo = 0
        self._prev_frame_index = 0

    @override
    def on_create(self) -> None:
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

    @override
    def begin(self) -> Tuple[bool, bool]:
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        result = super().begin()
        imgui.pop_style_var()
        return result

    @override
    def on_destroy(self) -> None:
        assert self._texture != 0
        assert self._pbo != 0

        GL.glDeleteTextures(1, self._texture)
        self._texture = 0

        GL.glDeleteBuffers(1, self._pbo)
        self._pbo = 0

    @override
    def on_process(self) -> None:
        self.begin_child_canvas()
        try:
            self.on_canvas()
            self.on_popup_menu()
        finally:
            imgui.end_child()

    def update_texture(self) -> None:
        if not self._texture:
            return

        process = self.context.pm.get(self.window_config.uuid)
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

    @staticmethod
    def begin_child_canvas() -> None:
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (0, 0))
        imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, 0.5, 0.5, 0.5)
        child_flags = _WINDOW_NO_MOVE | _WINDOW_NO_SCROLLBAR | _WINDOW_NO_RESIZE
        imgui.begin_child("Canvas", 0, 0, border=True, flags=child_flags)  # noqa
        imgui.pop_style_color()
        imgui.pop_style_var()

    def on_canvas(self):
        cx, cy = imgui.get_cursor_screen_pos()
        cw, ch = imgui.get_content_region_available()

        draw_list = get_window_draw_list()
        filled_color = imgui.get_color_u32_rgba(*self._clear_color)
        draw_list.add_rect_filled(cx, cy, cx + cw, cy + cy, filled_color)

        self.update_texture()

        p1 = cx, cy
        p2 = cx + cw, cy + ch
        draw_list.add_image(self._texture, p1, p2, (0, 0), (1, 1))

    def on_popup_menu(self):
        if not imgui.begin_popup_context_window().opened:
            return

        try:
            imgui.separator()
            if menu_item("Close"):
                self.opened = False
        finally:
            imgui.end_popup()
