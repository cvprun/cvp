# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class InRangeNode(OpenCVFunctionNode):
    """Check if image pixels are within specified range."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source image",
        )
        lowerb_pin = DataInputPin(
            name=PinName("lowerb"),
            dtype=Dtype.any(),
            docs="Lower boundary",
        )
        upperb_pin = DataInputPin(
            name=PinName("upperb"),
            dtype=Dtype.any(),
            docs="Upper boundary",
        )
        super().__init__("inRange", src_pin, lowerb_pin, upperb_pin)

    def apply_function(self, src, lowerb, upperb, **kwargs) -> Any:
        return cv2.inRange(src, lowerb, upperb)
