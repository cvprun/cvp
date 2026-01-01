# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class ConvertScaleAbsNode(OpenCVFunctionNode):
    """Convert array to 8-bit unsigned integers with scaling and absolute value."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source image",
        )
        alpha_pin = DataInputPin(
            name=PinName("alpha"),
            dtype=Dtype(float),
            docs="Scale factor",
            default=1.0,
        )
        beta_pin = DataInputPin(
            name=PinName("beta"),
            dtype=Dtype(float),
            docs="Delta added to scaled values",
            default=0.0,
        )
        super().__init__("convertScaleAbs", src_pin, alpha_pin, beta_pin)

    def apply_function(self, src, alpha, beta, **kwargs) -> Any:
        return cv2.convertScaleAbs(src, alpha=alpha, beta=beta)
