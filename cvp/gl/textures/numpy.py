# -*- coding: utf-8 -*-

from os import PathLike
from typing import IO, Any, Literal, Optional, Tuple, Union
from weakref import finalize

import numpy as np
from numpy import full, ndarray, uint8, zeros
from numpy.typing import NDArray
from PIL.Image import Image
from PIL.Image import fromarray as pillow_from_array
from PIL.Image import open as pillow_open

from cvp.gl.textures.data_type import TextureDataType
from cvp.gl.textures.filter import TextureMagFilter, TextureMinFilter
from cvp.gl.textures.format import TextureFormat
from cvp.gl.textures.internal_format import TextureInternalFormat
from cvp.gl.textures.texture import Texture
from cvp.gl.textures.wrap import TextureWrap
from cvp.types.colors import BLACK_RGBA

FilePathLike = Union[str, bytes, PathLike[str], PathLike[bytes], IO[bytes]]


def _close_texture(texture: Texture) -> None:
    texture.close()


class NumpyTexture:
    _array: Optional[NDArray[uint8]]
    _texture: Optional[Texture]
    _finalizer: Optional[finalize]

    def __init__(self):
        self._array = None
        self._texture = None
        self._finalizer = None

    @classmethod
    def from_empty(cls, width: int, height: int, channels: int):
        result = cls()
        result.open_with_empty(width, height, channels)
        return result

    @classmethod
    def from_file(cls, file: FilePathLike):
        result = cls()
        result.open_with_file(file)
        return result

    @classmethod
    def from_numpy(cls, array: NDArray[uint8], *, use_deepcopy=False):
        result = cls()
        result.open_with_numpy(array, use_deepcopy=use_deepcopy)
        return result

    @property
    def opened(self) -> bool:
        return self._array is not None

    @classmethod
    def _create_texture(
        cls,
        array: NDArray[uint8],
        *,
        min_filter=TextureMinFilter.nearest_mipmap_nearest,
        mag_filter=TextureMagFilter.nearest,
        wrap_s=TextureWrap.clamp_to_border,
        wrap_t=TextureWrap.clamp_to_border,
        use_mipmaps=True,
        border_color=BLACK_RGBA,
        level_of_detail=Texture.BASE_IMAGE_LEVEL,
        border_width: Literal[0, 1] = 0,
    ):
        if len(array.shape) == 2:
            internal_format = TextureInternalFormat.luminance8
            pix_format = TextureFormat.luminance
        elif len(array.shape) == 3:
            channels = array.shape[2]
            if channels == 3:
                internal_format = TextureInternalFormat.rgb8
                pix_format = TextureFormat.rgb
            elif channels == 4:
                internal_format = TextureInternalFormat.rgba8
                pix_format = TextureFormat.rgba
            else:
                raise ValueError(f"Invalid number of channels: {channels}")
        else:
            raise ValueError(f"Invalid number of shape: {len(array.shape)}")

        width = array.shape[1]
        height = array.shape[0]
        size = width, height
        pixels = array.tobytes()
        data_type = TextureDataType.from_dtype(array.dtype)

        return Texture(
            size=size,
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

    def open_with_empty(self, width: int, height: int, channels: int) -> None:
        self.open_with_numpy(zeros((height, width, channels), dtype=uint8))

    def open_with_filled(
        self,
        width: int,
        height: int,
        channels: int,
        color: Any,
    ) -> None:
        self.open_with_numpy(full((height, width, channels), color, dtype=uint8))

    def open_with_file(self, file: FilePathLike) -> None:
        self.open_with_pillow(pillow_open(file))

    def open_with_pillow(self, image: Image) -> None:
        if self._array is not None:
            raise ValueError("Image not closed")

        assert self._texture is None
        assert self._finalizer is None

        self._array = np.array(image)
        self._texture = self._create_texture(self._array)
        self._finalizer = finalize(self, _close_texture, self._texture)

        assert self._array is not None
        assert self._texture is not None
        assert self._finalizer is not None

    def open_with_numpy(self, array: NDArray[uint8], *, use_deepcopy=False) -> None:
        if self._array is not None:
            raise ValueError("Image not closed")

        assert self._texture is None
        assert self._finalizer is None

        self._array = array.copy() if use_deepcopy else array
        self._texture = self._create_texture(self._array)
        self._finalizer = finalize(self, _close_texture, self._texture)

        assert self._array is not None
        assert self._texture is not None
        assert self._finalizer is not None

    def close(self) -> None:
        if self._array is None:
            raise ValueError("Image not opened")

        assert self._texture is not None
        assert self._finalizer is not None
        if self._finalizer.detach():
            _close_texture(self._texture)

        self._array = None
        self._texture = None
        self._finalizer = None

    @property
    def array(self):
        if self._array is None:
            raise ValueError("Image not opened")
        assert isinstance(self._array, ndarray)
        return self._array

    @property
    def texture(self) -> Texture:
        if self._texture is None:
            raise ValueError("Image not opened")
        return self._texture

    @property
    def texture_id(self) -> int:
        return self._texture.texture_id if self._texture is not None else 0

    @property
    def height(self) -> int:
        if self._array is None:
            return 0
        if len(self._array.shape) <= 0:
            return 0
        return self._array.shape[0]

    @property
    def width(self) -> int:
        if self._array is None:
            return 0
        if len(self._array.shape) <= 1:
            return 0
        return self._array.shape[1]

    @property
    def size(self) -> Tuple[int, int]:
        return self.width, self.height

    def as_pillow_image(self):
        return pillow_from_array(self._array)

    def commit(self) -> None:
        with self.texture:
            self.texture.update_pixels(self.array.tobytes())

    def fetch(self) -> None:
        with self.texture:
            self.texture.get_pixels(array=self.array)
