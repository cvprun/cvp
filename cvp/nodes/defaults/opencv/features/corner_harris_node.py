# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class CornerHarrisNode(OpenCVFunctionNode):
    """Apply Harris corner detection."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source grayscale image",
        )
        blocksize_pin = DataInputPin(
            name=PinName("blockSize"),
            dtype=Dtype(int),
            docs="Size of the neighborhood for corner detection",
            default=2,
        )
        ksize_pin = DataInputPin(
            name=PinName("ksize"),
            dtype=Dtype(int),
            docs="Aperture parameter for Sobel operator",
            default=3,
        )
        k_pin = DataInputPin(
            name=PinName("k"),
            dtype=Dtype(float),
            docs="Harris detector free parameter",
            default=0.04,
        )
        bordertype_pin = DataInputPin(
            name=PinName("borderType"),
            dtype=Dtype(int),
            docs="Border extrapolation type",
            default=cv2.BORDER_DEFAULT,
        )
        super().__init__(
            "cornerHarris", src_pin, blocksize_pin, ksize_pin, k_pin, bordertype_pin
        )

    def apply_function(self, src, blockSize, ksize, k, borderType, **kwargs) -> Any:
        return cv2.cornerHarris(src, blockSize, ksize, k, borderType=borderType)
