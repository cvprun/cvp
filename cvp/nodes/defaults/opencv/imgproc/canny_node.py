# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class CannyNode(OpenCVFunctionNode):
    """Apply Canny edge detection."""

    def __init__(self):
        image_pin = DataInputPin(
            name=PinName("image"),
            dtype=Dtype.any(),
            docs="Source image (grayscale)",
        )
        threshold1_pin = DataInputPin(
            name=PinName("threshold1"),
            dtype=Dtype(float),
            docs="First threshold for edge detection",
            default=100.0,
        )
        threshold2_pin = DataInputPin(
            name=PinName("threshold2"),
            dtype=Dtype(float),
            docs="Second threshold for edge detection",
            default=200.0,
        )
        aperturesize_pin = DataInputPin(
            name=PinName("apertureSize"),
            dtype=Dtype(int),
            docs="Aperture size for Sobel operator",
            default=3,
        )
        l2gradient_pin = DataInputPin(
            name=PinName("L2gradient"),
            dtype=Dtype(bool),
            docs="Use L2 norm for gradient magnitude",
            default=False,
        )
        super().__init__(
            "Canny",
            image_pin,
            threshold1_pin,
            threshold2_pin,
            aperturesize_pin,
            l2gradient_pin,
        )

    def apply_function(
        self, image, threshold1, threshold2, apertureSize, L2gradient, **kwargs
    ) -> Any:
        return cv2.Canny(
            image,
            threshold1,
            threshold2,
            apertureSize=apertureSize,
            L2gradient=L2gradient,
        )
