# -*- coding: utf-8 -*-

from ctypes import c_void_p
from typing import Final, Literal, Optional, Union

from OpenGL import GL

from cvp.gl.textures.data_type import TextureDataType, texture_data_type_mapping
from cvp.gl.textures.filter import TextureFilter, texture_filter_mapping
from cvp.gl.textures.format import (
    TextureFormat,
    texture_format_channels_mapping,
    texture_format_mapping,
)
from cvp.gl.textures.internal_format import (
    TextureInternalFormat,
    texture_internal_format_mapping,
)
from cvp.gl.textures.wrap import TextureWrap, texture_wrap_mapping
from cvp.types.colors import BLACK_RGBA
from cvp.types.shapes_i import SizeI


class Texture:
    BASE_IMAGE_LEVEL: Final[int] = 0

    INTERNAL_FORMAT_MAPPING = texture_internal_format_mapping()
    FORMAT_MAPPING = texture_format_mapping()
    FORMAT_CHANNELS_MAPPING = texture_format_channels_mapping()
    DATA_TYPE_MAPPING = texture_data_type_mapping()
    FILTER_MAPPING = texture_filter_mapping()
    WRAP_MAPPING = texture_wrap_mapping()

    _id: Union[int, GL.Constant]

    def __init__(
        self,
        size: Optional[SizeI] = None,
        *,
        internal_format=TextureInternalFormat.rgba8,
        pix_format=TextureFormat.rgb,
        data_type=TextureDataType.unsigned_byte,
        min_filter=TextureFilter.linear,
        mag_filter=TextureFilter.linear,
        wrap_s=TextureWrap.repeat,
        wrap_t=TextureWrap.repeat,
        border_color=BLACK_RGBA,
        use_mipmaps=False,
    ):
        self._width = 0
        self._height = 0

        self._internal_format = internal_format
        self._pix_format = pix_format
        self._data_type = data_type
        self._min_filter = min_filter
        self._mag_filter = mag_filter
        self._wrap_s = wrap_s
        self._wrap_t = wrap_t
        self._border_color = border_color
        self._use_mipmaps = use_mipmaps

        self._id = 0
        self._bound = False

        if size is not None:
            self.open(size[0], size[1])

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def size(self) -> SizeI:
        return self._width, self._height

    @property
    def texture_id(self) -> int:
        return int(self._id)

    @property
    def bound(self) -> bool:
        return self._bound

    @property
    def opened(self) -> bool:
        return self._id != 0

    def __bool__(self) -> bool:
        return self.opened

    def open(
        self,
        width: int,
        height: int,
        pixels: Optional[bytes] = None,
        *,
        internal_format=TextureInternalFormat.rgba8,
        pix_format=TextureFormat.rgb,
        data_type=TextureDataType.unsigned_byte,
        min_filter=TextureFilter.linear,
        mag_filter=TextureFilter.linear,
        wrap_s=TextureWrap.repeat,
        wrap_t=TextureWrap.repeat,
        use_mipmaps=False,
        border_color=BLACK_RGBA,
        level_of_detail=BASE_IMAGE_LEVEL,
        border_width: Literal[0, 1] = 0,
    ) -> None:
        if self._id != 0:
            raise ValueError("Texture is already opened")

        if width <= 0 or height <= 0:
            raise ValueError("Invalid texture size")

        # The width of the texture image. Must be 2n + 2(border) for some integer n.
        # The height of the texture image. Must be 2^m + 2(border) for some integer m.

        texture_id = GL.glGenTextures(1)
        assert texture_id != 0

        gl_internal_format = self.INTERNAL_FORMAT_MAPPING[internal_format]
        gl_format = self.FORMAT_MAPPING[pix_format]
        gl_min_f = self.FILTER_MAPPING[min_filter]
        gl_mag_f = self.FILTER_MAPPING[mag_filter]
        gl_wrap_s = self.WRAP_MAPPING[wrap_s]
        gl_wrap_t = self.WRAP_MAPPING[wrap_t]
        gl_type = self.DATA_TYPE_MAPPING[data_type]

        is_wrap_s_border = wrap_s == TextureWrap.clamp_to_border
        is_wrap_t_border = wrap_t == TextureWrap.clamp_to_border
        is_border_color_required = is_wrap_s_border or is_wrap_t_border

        GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)
        try:
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, gl_min_f)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, gl_mag_f)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, gl_wrap_s)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, gl_wrap_t)

            if is_border_color_required:
                GL.glTexParameterfv(
                    GL.GL_TEXTURE_2D,
                    GL.GL_TEXTURE_BORDER_COLOR,
                    border_color,
                )

            GL.glTexImage2D(
                GL.GL_TEXTURE_2D,
                level_of_detail,
                gl_internal_format,
                width,
                height,
                border_width,
                gl_format,
                gl_type,
                pixels or c_void_p(0),
            )

            if use_mipmaps:
                GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

            self._width = width
            self._height = height

            self._internal_format = internal_format
            self._pix_format = pix_format
            self._data_type = data_type
            self._min_filter = min_filter
            self._mag_filter = mag_filter
            self._wrap_s = wrap_s
            self._wrap_t = wrap_t
            self._border_color = border_color
            self._use_mipmaps = use_mipmaps

            self._id = texture_id
            self._bound = False
        finally:
            GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def close(self) -> None:
        if self._id == 0:
            raise ValueError("Texture is not opened")

        GL.glDeleteTextures(1, self._id)
        self._id = 0

    def bind(self) -> None:
        if self._bound:
            raise ValueError("Texture is already bound")

        GL.glBindTexture(GL.GL_TEXTURE_2D, self._id)
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

    def update_with_rgb_pixels(self, pixels: Optional[bytes] = None) -> None:
        self._update_texture(GL.GL_RGB, pixels)

    def update_with_alpha_pixels(self, pixels: Optional[bytes] = None) -> None:
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
