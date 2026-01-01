# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class AddWeightedNode(OpenCVFunctionNode):
    """Calculate weighted sum of two images."""

    def __init__(self):
        src1_pin = DataInputPin(
            name=PinName("src1"),
            dtype=Dtype.any(),
            docs="First source image",
        )
        alpha_pin = DataInputPin(
            name=PinName("alpha"),
            dtype=Dtype(float),
            docs="Weight of first image",
            default=0.5,
        )
        src2_pin = DataInputPin(
            name=PinName("src2"),
            dtype=Dtype.any(),
            docs="Second source image",
        )
        beta_pin = DataInputPin(
            name=PinName("beta"),
            dtype=Dtype(float),
            docs="Weight of second image",
            default=0.5,
        )
        gamma_pin = DataInputPin(
            name=PinName("gamma"),
            dtype=Dtype(float),
            docs="Scalar added to each sum",
            default=0.0,
        )
        super().__init__(
            "addWeighted", src1_pin, alpha_pin, src2_pin, beta_pin, gamma_pin
        )

    def apply_function(self, src1, alpha, src2, beta, gamma, **kwargs) -> Any:
        return cv2.addWeighted(src1, alpha, src2, beta, gamma)
