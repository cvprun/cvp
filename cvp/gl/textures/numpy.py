# -*- coding: utf-8 -*-

from os import PathLike
from typing import IO, Optional, Tuple, Union
from weakref import finalize

import numpy as np
from numpy import ndarray, uint8, zeros
from numpy.typing import NDArray
from PIL import Image

from cvp.gl.textures.texture import Texture

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

    def open_with_empty(self, width: int, height: int, channels: int) -> None:
        if self._array is not None:
            raise ValueError("Image not closed")

        assert self._texture is None
        assert self._finalizer is None
        self._array = zeros((height, width, channels), dtype=uint8)
        self._texture = Texture()
        self._texture.open(width, height)
        self._finalizer = finalize(self, _close_texture, self._texture)

    def open_with_file(self, file: FilePathLike) -> None:
        if self._array is not None:
            raise ValueError("Image not closed")

        assert self._texture is None
        assert self._finalizer is None
        image = Image.open(file)
        self._array = np.array(image)
        self._texture = Texture()
        self._texture.open(image.width, image.height)
        self._finalizer = finalize(self, _close_texture, self._texture)

    def open_with_numpy(self, array: NDArray[uint8], *, use_deepcopy=False) -> None:
        if self._array is not None:
            raise ValueError("Image not closed")

        assert isinstance(array, ndarray)
        assert self._texture is None
        assert self._finalizer is None
        self._array = array.copy() if use_deepcopy else array
        self._texture = Texture()
        self._texture.open(self._array.shape[1], self._array.shape[0])
        self._finalizer = finalize(self, _close_texture, self._texture)

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
        if self._array is not None:
            raise ValueError("Image not closed")
        assert isinstance(self._array, ndarray)
        return self._array

    @property
    def texture_id(self) -> int:
        return self._texture.texture if self._texture else 0

    @property
    def height(self) -> int:
        return self.array.shape[0]

    @property
    def width(self) -> int:
        return self.array.shape[1]

    @property
    def size(self) -> Tuple[int, int]:
        return self.width, self.height

    def as_pillow_image(self):
        return Image.fromarray(self._array)
