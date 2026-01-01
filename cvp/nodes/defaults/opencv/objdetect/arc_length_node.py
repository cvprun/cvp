# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class ArcLengthNode(OpenCVFunctionNode):
    """Calculate contour perimeter."""

    def __init__(self):
        curve_pin = DataInputPin(
            name=PinName("curve"),
            dtype=Dtype.any(),
            docs="Input contour or curve",
        )
        closed_pin = DataInputPin(
            name=PinName("closed"),
            dtype=Dtype(bool),
            docs="Whether the curve is closed",
            default=True,
        )
        super().__init__("arcLength", curve_pin, closed_pin)

    def apply_function(self, curve, closed, **kwargs) -> Any:
        return cv2.arcLength(curve, closed)
