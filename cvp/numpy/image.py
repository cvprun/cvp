# -*- coding: utf-8 -*-

from typing import Any

from numpy import full, ndarray, uint8, zeros
from numpy.random import randint
from numpy.typing import NDArray


def make_image(width: int, height: int, channels: int, data: bytes) -> NDArray[uint8]:
    return ndarray((height, width, channels), dtype=uint8, buffer=data)


def make_image_filled(
    width: int,
    height: int,
    channels: int,
    color: Any,
) -> NDArray[uint8]:
    return full((height, width, channels), color, dtype=uint8)


def make_image_empty(width: int, height: int, channels: int) -> NDArray[uint8]:
    return zeros((height, width, channels), dtype=uint8)


def make_image_random(width: int, height: int, channels: int) -> NDArray[uint8]:
    return randint(low=0, high=256, size=(height, width, channels), dtype=uint8)
