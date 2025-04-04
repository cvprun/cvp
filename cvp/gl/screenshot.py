# -*- coding: utf-8 -*-

from typing import Literal

from numpy import flipud, frombuffer, uint8
from numpy.typing import NDArray
from OpenGL import GL
from PIL.Image import Image, fromarray


def screenshot_as_pixels(
    width: int,
    height: int,
    *,
    x=0,
    y=0,
    channels: Literal[3, 4] = 4,
) -> bytes:
    pixel_format = GL.GL_RGB if channels == 3 else GL.GL_RGBA
    GL.glReadBuffer(GL.GL_FRONT)
    result = GL.glReadPixels(x, y, width, height, pixel_format, GL.GL_UNSIGNED_BYTE)
    assert isinstance(result, bytes)
    return result


def screenshot_as_numpy(
    width: int,
    height: int,
    *,
    x=0,
    y=0,
    channels: Literal[3, 4] = 4,
) -> NDArray[uint8]:
    pixels = screenshot_as_pixels(width, height, x=x, y=y, channels=channels)
    image = frombuffer(pixels, dtype=uint8).reshape(height, width, channels)
    # The OpenGL coordinate system and the image coordinate system are opposites.
    return flipud(image)


def screenshot_as_pillow(
    width: int,
    height: int,
    *,
    x=0,
    y=0,
    channels: Literal[3, 4] = 4,
) -> Image:
    array = screenshot_as_numpy(width, height, x=x, y=y, channels=channels)
    return fromarray(array)
