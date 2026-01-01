# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class NormNode(OpenCVFunctionNode):
    """Calculate norm of an array."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src1"),
            dtype=Dtype.any(),
            docs="Source image",
        )
        normtype_pin = DataInputPin(
            name=PinName("normType"),
            dtype=Dtype(int),
            docs="Norm type (cv2.NORM_*)",
            default=cv2.NORM_L2,
        )
        super().__init__("norm", src_pin, normtype_pin)

    def apply_function(self, src1, normType, **kwargs) -> Any:
        return cv2.norm(src1, normType=normType)
