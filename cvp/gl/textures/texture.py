# -*- coding: utf-8 -*-

from ctypes import c_void_p
from typing import Final, Literal, Optional, Union

from OpenGL import GL

from cvp.gl.textures.data_type import (
    TextureDataType,
    texture_data_type_mapping,
    texture_numpy_dtype_mapping,
)
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
from cvp.types.colors import BLACK_RGBA, RGBA
from cvp.types.shapes_i import SizeI


class Texture:
    BASE_IMAGE_LEVEL: Final[int] = 0

    INTERNAL_FORMAT_MAPPING = texture_internal_format_mapping()
    FORMAT_MAPPING = texture_format_mapping()
    FORMAT_CHANNELS_MAPPING = texture_format_channels_mapping()
    DATA_TYPE_MAPPING = texture_data_type_mapping()
    NUMPY_DTYPE_MAPPING = texture_numpy_dtype_mapping()
    FILTER_MAPPING = texture_filter_mapping()
    WRAP_MAPPING = texture_wrap_mapping()

    _id: Union[int, GL.Constant]

    def __init__(
        self,
        size: Optional[SizeI] = None,
        pixels: Optional[bytes] = None,
        *,
        internal_format=TextureInternalFormat.rgba8,
        pix_format=TextureFormat.rgba,
        data_type=TextureDataType.unsigned_byte,
        min_filter=TextureFilter.linear,
        mag_filter=TextureFilter.linear,
        wrap_s=TextureWrap.repeat,
        wrap_t=TextureWrap.repeat,
        use_mipmaps=False,
        border_color=BLACK_RGBA,
        level_of_detail=BASE_IMAGE_LEVEL,
        border_width: Literal[0, 1] = 0,
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
            self.open(
                width=size[0],
                height=size[1],
                pixels=pixels,
                internal_format=internal_format,
                pix_format=pix_format,
                data_type=data_type,
                min_filter=min_filter,
                mag_filter=mag_filter,
                wrap_s=wrap_s,
                wrap_t=wrap_t,
                use_mipmaps=use_mipmaps,
                border_color=border_color,
                level_of_detail=level_of_detail,
                border_width=border_width,
            )

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
    def internal_format(self):
        return self._internal_format

    @property
    def pix_format(self):
        return self._pix_format

    @property
    def channels(self):
        return self.FORMAT_CHANNELS_MAPPING[self._pix_format]

    @property
    def data_type(self):
        return self._data_type

    @property
    def numpy_dtype(self):
        return self.NUMPY_DTYPE_MAPPING[self._data_type]

    @property
    def min_filter(self):
        return self._min_filter

    @property
    def mag_filter(self):
        return self._mag_filter

    @property
    def wrap_s(self):
        return self._wrap_s

    @property
    def wrap_t(self):
        return self._wrap_t

    @property
    def texture_id(self) -> int:
        return int(self._id)

    @property
    def opened(self) -> bool:
        return self._id != 0

    @property
    def bound(self) -> bool:
        return self._bound

    def __bool__(self) -> bool:
        return self.opened

    def open(
        self,
        width: int,
        height: int,
        pixels: Optional[bytes] = None,
        *,
        internal_format=TextureInternalFormat.rgba8,
        pix_format=TextureFormat.rgba,
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
        gl_type = self.DATA_TYPE_MAPPING[data_type]

        gl_min_f = self.FILTER_MAPPING[min_filter]
        gl_mag_f = self.FILTER_MAPPING[mag_filter]
        gl_wrap_s = self.WRAP_MAPPING[wrap_s]
        gl_wrap_t = self.WRAP_MAPPING[wrap_t]

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

        GL.glDeleteTextures(1, [self._id])
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

    def set_min_filter(self, min_filter: TextureFilter) -> None:
        if not self._bound:
            raise ValueError("Texture is not bound")

        if min_filter == self._min_filter:
            return

        gl_min_f = self.FILTER_MAPPING[min_filter]
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, gl_min_f)
        self._min_filter = min_filter

    def set_mag_filter(self, mag_filter: TextureFilter) -> None:
        if not self._bound:
            raise ValueError("Texture is not bound")

        if mag_filter == self._mag_filter:
            return

        gl_mag_f = self.FILTER_MAPPING[mag_filter]
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, gl_mag_f)
        self._mag_filter = mag_filter

    def set_wrap_s(self, wrap_s: TextureWrap) -> None:
        if not self._bound:
            raise ValueError("Texture is not bound")

        if wrap_s == self._wrap_s:
            return

        gl_wrap_s = self.WRAP_MAPPING[wrap_s]
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, gl_wrap_s)
        self._wrap_s = wrap_s

    def set_wrap_t(self, wrap_t: TextureWrap) -> None:
        if not self._bound:
            raise ValueError("Texture is not bound")

        if wrap_t == self._wrap_t:
            return

        gl_wrap_t = self.WRAP_MAPPING[wrap_t]
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, gl_wrap_t)
        self._wrap_t = wrap_t

    def set_border_color(self, color: RGBA) -> None:
        if not self._bound:
            raise ValueError("Texture is not bound")

        if color == self._border_color:
            return

        GL.glTexParameterfv(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_BORDER_COLOR, color)
        self._border_color = color

    def generate_mipmap(self) -> None:
        if not self._bound:
            raise ValueError("Texture is not bound")

        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

    def update_pixels(
        self,
        pixels: bytes,
        pix_format: Optional[TextureFormat] = None,
        data_type: Optional[TextureDataType] = None,
        *,
        level_of_detail=BASE_IMAGE_LEVEL,
        border_width: Literal[0, 1] = 0,
    ) -> None:
        if not self._bound:
            raise ValueError("Texture is not bound")

        pix_format = pix_format or self._pix_format
        assert pix_format is not None

        data_type = data_type or self._data_type
        assert data_type is not None

        gl_pix_format = self.FORMAT_MAPPING[pix_format]
        gl_data_type = self.DATA_TYPE_MAPPING[data_type]

        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            level_of_detail,
            self.INTERNAL_FORMAT_MAPPING[self._internal_format],
            self._width,
            self._height,
            border_width,
            gl_pix_format,
            gl_data_type,
            pixels,
        )

        if self._use_mipmaps:
            GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

    def update_rgb_pixels(
        self,
        pixels: bytes,
        data_type=TextureDataType.unsigned_byte,
    ) -> None:
        self.update_pixels(pixels, TextureFormat.rgb, data_type)

    def update_rgba_pixels(
        self,
        pixels: bytes,
        data_type=TextureDataType.unsigned_byte,
    ) -> None:
        self.update_pixels(pixels, TextureFormat.rgba, data_type)

    def update_alpha_pixels(
        self,
        pixels: bytes,
        data_type=TextureDataType.unsigned_byte,
    ) -> None:
        self.update_pixels(pixels, TextureFormat.alpha, data_type)

    def clear(self, *, level_of_detail=BASE_IMAGE_LEVEL) -> None:
        if not self._bound:
            raise ValueError("Texture is not bound")

        GL.glTexSubImage2D(
            GL.GL_TEXTURE_2D,
            level_of_detail,
            0,
            0,
            self._width,
            self._height,
            self.FORMAT_MAPPING[self._pix_format],
            self.DATA_TYPE_MAPPING[self._data_type],
            c_void_p(0),
        )

        if self._use_mipmaps:
            GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

    def update_sub_pixels(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        pixels: bytes,
        pix_format: Optional[TextureFormat] = None,
        data_type: Optional[TextureDataType] = None,
        *,
        level_of_detail=BASE_IMAGE_LEVEL,
    ) -> None:
        if not self._bound:
            raise ValueError("Texture is not bound")

        pix_format = pix_format or self._pix_format
        assert pix_format is not None

        data_type = data_type or self._data_type
        assert data_type is not None

        gl_pix_format = self.FORMAT_MAPPING[pix_format]
        gl_data_type = self.DATA_TYPE_MAPPING[data_type]

        GL.glTexSubImage2D(
            GL.GL_TEXTURE_2D,
            level_of_detail,
            x,
            y,
            width,
            height,
            gl_pix_format,
            gl_data_type,
            pixels,
        )

        if self._use_mipmaps:
            GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

    def get_pixels(
        self,
        pix_format: Optional[TextureFormat] = None,
        data_type: Optional[TextureDataType] = None,
        *,
        level_of_detail=BASE_IMAGE_LEVEL,
    ) -> bytes:
        if not self._bound:
            raise ValueError("Texture is not bound")

        pix_format = pix_format or self._pix_format
        assert pix_format is not None

        data_type = data_type or self._data_type
        assert data_type is not None

        gl_pix_format = self.FORMAT_MAPPING[pix_format]
        gl_data_type = self.DATA_TYPE_MAPPING[data_type]

        result = GL.glGetTexImage(
            GL.GL_TEXTURE_2D,
            level_of_detail,
            gl_pix_format,
            gl_data_type,
        )

        assert isinstance(result, bytes)
        return result
