# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class ApproxPolyDPNode(OpenCVFunctionNode):
    """Approximate contour with fewer vertices."""

    def __init__(self):
        curve_pin = DataInputPin(
            name=PinName("curve"),
            dtype=Dtype.any(),
            docs="Input contour",
        )
        epsilon_pin = DataInputPin(
            name=PinName("epsilon"),
            dtype=Dtype(float),
            docs="Approximation accuracy",
            default=0.02,
        )
        closed_pin = DataInputPin(
            name=PinName("closed"),
            dtype=Dtype(bool),
            docs="Whether the curve is closed",
            default=True,
        )
        super().__init__("approxPolyDP", curve_pin, epsilon_pin, closed_pin)

    def apply_function(self, curve, epsilon, closed, **kwargs) -> Any:
        return cv2.approxPolyDP(curve, epsilon, closed)
