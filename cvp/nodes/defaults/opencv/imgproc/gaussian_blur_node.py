# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class GaussianBlurNode(OpenCVFunctionNode):
    """Apply Gaussian blur filter."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source image",
        )
        ksize_pin = DataInputPin(
            name=PinName("ksize"),
            dtype=Dtype.any(),
            docs="Gaussian kernel size (width, height)",
            default=(5, 5),
        )
        sigmax_pin = DataInputPin(
            name=PinName("sigmaX"),
            dtype=Dtype(float),
            docs="Gaussian kernel standard deviation in X direction",
            default=0.0,
        )
        sigmay_pin = DataInputPin(
            name=PinName("sigmaY"),
            dtype=Dtype(float),
            docs="Gaussian kernel standard deviation in Y direction",
            default=0.0,
        )
        bordertype_pin = DataInputPin(
            name=PinName("borderType"),
            dtype=Dtype(int),
            docs="Border extrapolation type",
            default=cv2.BORDER_DEFAULT,
        )
        super().__init__(
            "GaussianBlur", src_pin, ksize_pin, sigmax_pin, sigmay_pin, bordertype_pin
        )

    def apply_function(self, src, ksize, sigmaX, sigmaY, borderType, **kwargs) -> Any:
        return cv2.GaussianBlur(
            src, ksize, sigmaX, sigmaY=sigmaY, borderType=borderType
        )
