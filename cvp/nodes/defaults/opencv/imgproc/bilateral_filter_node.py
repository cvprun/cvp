# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class BilateralFilterNode(OpenCVFunctionNode):
    """Apply bilateral filter for noise removal while keeping edges sharp."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source image",
        )
        d_pin = DataInputPin(
            name=PinName("d"),
            dtype=Dtype(int),
            docs="Diameter of pixel neighborhood",
            default=9,
        )
        sigmacolor_pin = DataInputPin(
            name=PinName("sigmaColor"),
            dtype=Dtype(float),
            docs="Filter sigma in color space",
            default=75.0,
        )
        sigmaspace_pin = DataInputPin(
            name=PinName("sigmaSpace"),
            dtype=Dtype(float),
            docs="Filter sigma in coordinate space",
            default=75.0,
        )
        bordertype_pin = DataInputPin(
            name=PinName("borderType"),
            dtype=Dtype(int),
            docs="Border extrapolation type",
            default=cv2.BORDER_DEFAULT,
        )
        super().__init__(
            "bilateralFilter",
            src_pin,
            d_pin,
            sigmacolor_pin,
            sigmaspace_pin,
            bordertype_pin,
        )

    def apply_function(
        self, src, d, sigmaColor, sigmaSpace, borderType, **kwargs
    ) -> Any:
        return cv2.bilateralFilter(
            src, d, sigmaColor, sigmaSpace, borderType=borderType
        )
