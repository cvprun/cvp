# -*- coding: utf-8 -*-

from typing import Final, Tuple

from numpy import bool_ as np_bool
from numpy import concatenate, equal, uint8, where
from numpy.typing import NDArray

BLACK_COLOR: Final[Tuple[int, int, int]] = 0, 0, 0
DEFAULT_CHROMA_COLOR: Final[Tuple[int, int, int]] = BLACK_COLOR

CHANNEL_MIN: Final[int] = 0
CHANNEL_MAX: Final[int] = 255


def generate_mask(image: NDArray, chroma_color=DEFAULT_CHROMA_COLOR) -> NDArray:
    assert image.dtype == uint8
    assert len(image.shape) == 3
    assert image.shape[-1] == 3

    channels_cmp: NDArray[np_bool] = equal(image, chroma_color)
    pixel_cmp: NDArray[np_bool] = channels_cmp.all(axis=-1, keepdims=True)
    return where(pixel_cmp, CHANNEL_MIN, CHANNEL_MAX).astype(uint8)


def split_mask_on_off(mask: NDArray) -> Tuple[NDArray, NDArray]:
    assert len(mask.shape) == 3
    assert mask.shape[-1] == 1

    mask_cmp: NDArray[np_bool] = mask != 0  # noqa
    mask_on = mask_cmp.astype(uint8)
    mask_off = 1 - mask_on

    assert len(mask_on.shape) == 3
    assert mask_on.shape[-1] == 1
    assert mask_on.dtype == uint8

    assert len(mask_off.shape) == 3
    assert mask_off.shape[-1] == 1
    assert mask_off.dtype == uint8

    return mask_on, mask_off  # type: ignore[return-value]


def merge_to_bgra32(image: NDArray, mask: NDArray) -> NDArray:
    assert image.dtype == uint8
    assert len(image.shape) == 3
    assert image.shape[-1] == 3

    assert mask.dtype == uint8
    assert len(mask.shape) == 3
    assert mask.shape[-1] == 1

    return concatenate((image, mask), axis=-1)
