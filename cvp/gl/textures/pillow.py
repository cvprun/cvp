# -*- coding: utf-8 -*-

import os
from os import PathLike
from typing import IO, Optional, Union
from weakref import finalize

import numpy as np
from numpy import uint8
from numpy.typing import NDArray
from PIL.Image import Image
from PIL.Image import fromarray as pil_image_from_array
from PIL.Image import open as pil_image_open
from PIL.ImageFile import ImageFile

from cvp.gl.textures.texture import Texture

FilePathLike = Union[str, bytes, PathLike[str], PathLike[bytes], IO[bytes]]


def open_file(path: FilePathLike) -> ImageFile:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Not found regular file: '{path}'")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"Not readable file: '{path}'")
    return pil_image_open(path)


def close_file(image: Image, texture: Texture) -> None:
    image.close()
    texture.close()


class PillowTexture:
    _image: Optional[Image]
    _texture: Optional[Texture]
    _finalizer: Optional[finalize]

    def __init__(self):
        self._image = None
        self._texture = None
        self._finalizer = None

    @classmethod
    def from_path(cls, path: FilePathLike):
        result = cls()
        result.open(path)
        return result

    @classmethod
    def from_numpy(cls, array: NDArray[uint8]):
        result = cls()
        result.open_with_numpy(array)
        return result

    def open(self, path: FilePathLike) -> None:
        if self._image is not None:
            raise ValueError("Image not closed")

        assert self._finalizer is None
        self._image = open_file(path)
        self._texture = Texture()
        self._texture.open(self._image.width, self._image.height)
        self._finalizer = finalize(self, close_file, self._image, self._texture)

    def open_with_numpy(self, array: NDArray[uint8]) -> None:
        if self._image is not None:
            raise ValueError("Image not closed")

        assert self._finalizer is None
        self._image = pil_image_from_array(array)
        self._texture = Texture()
        self._texture.open(self._image.width, self._image.height)
        self._finalizer = finalize(self, close_file, self._image, self._texture)

    def close(self) -> None:
        if self._image is None:
            raise ValueError("Image not opened")

        assert self._finalizer is not None
        if self._finalizer.detach():
            close_file(self._image, self._texture)

        self._image = None
        self._texture = None
        self._finalizer = None

    def as_numpy(self) -> NDArray[uint8]:
        return np.array(self._image)
