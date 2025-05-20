# -*- coding: utf-8 -*-

from typing import Final

from OpenGL import GL


class Framebuffer:
    BASE_MIPMAP_LEVEL: Final[int] = 0

    def __init__(self):
        self._id = 0
        self._bound = False

    @property
    def framebuffer_id(self) -> int:
        return int(self._id)

    @property
    def opened(self) -> bool:
        return self._id != 0

    @property
    def bound(self) -> bool:
        return self._bound

    def __bool__(self) -> bool:
        return self.opened

    def open(self) -> None:
        if self._id != 0:
            raise ValueError("Framebuffer is already opened")

        self._id = GL.glGenFramebuffers(1)
        assert self._id != 0

    def close(self) -> None:
        if self._id == 0:
            raise ValueError("Framebuffer is not opened")

        GL.glDeleteFramebuffers(1, [self._id])
        self._id = 0

    def bind(self) -> None:
        if self._bound:
            raise ValueError("Framebuffer is already bound")

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self._id)
        self._bound = True

    def release(self) -> None:
        if not self._bound:
            raise ValueError("Framebuffer is not bound")

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        self._bound = False

    def __enter__(self):
        self.bind()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def attach_texture(
        self,
        texture_id: int,
        *,
        level_of_detail=BASE_MIPMAP_LEVEL,
    ):
        if not self._bound:
            raise ValueError("Framebuffer is not bound")

        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER,
            GL.GL_COLOR_ATTACHMENT0,
            GL.GL_TEXTURE_2D,
            texture_id,
            level_of_detail,
        )
