# -*- coding: utf-8 -*-

from ctypes import c_void_p
from typing import Optional

from OpenGL import GL


class Texture:
    def __init__(self):
        self._width = 0
        self._height = 0
        self._texture = 0
        self._bound = False

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def texture(self):
        return self._texture

    @property
    def bound(self):
        return self._bound

    @property
    def opened(self) -> bool:
        return self._texture != 0

    def __bool__(self) -> bool:
        return self.opened

    def open(self, width: int, height: int) -> None:
        if self._texture != 0:
            raise ValueError("Texture is already opened")

        self._width = width
        self._height = height
        self._texture = GL.glGenTextures(1)
        assert self._texture != 0

        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_RGB,
            width,
            height,
            0,
            GL.GL_RGB,
            GL.GL_UNSIGNED_BYTE,
            None,
        )
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def close(self) -> None:
        if self._texture == 0:
            raise ValueError("Texture is not opened")

        GL.glDeleteTextures(1, self._texture)
        self._texture = 0

    def bind(self) -> None:
        if self._bound:
            raise ValueError("Texture is already bound")

        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)
        self._bound = True

    def release(self) -> None:
        if not self._bound:
            raise ValueError("Texture is not bound")

        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        self._bound = False

    def __enter__(self):
        self.bind()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def _update_texture(self, fmt: int, pixels: Optional[bytes] = None) -> None:
        assert self._bound, "Texture must be bound"

        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            fmt,
            self._width,
            self._height,
            0,
            fmt,
            GL.GL_UNSIGNED_BYTE,
            pixels,
        )

    def update_rgb_texture(self, pixels: Optional[bytes] = None) -> None:
        self._update_texture(GL.GL_RGB, pixels)

    def update_alpha_texture(self, pixels: Optional[bytes] = None) -> None:
        self._update_texture(GL.GL_ALPHA, pixels)

    def _clear_texture_sub_image_2d(self) -> None:
        assert self._bound, "Texture must be bound"

        GL.glTexSubImage2D(
            GL.GL_TEXTURE_2D,
            0,
            0,
            0,
            self._width,
            self._height,
            GL.GL_RGB,
            GL.GL_UNSIGNED_BYTE,
            c_void_p(0),
        )
