# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class GetRotationMatrix2DNode(OpenCVFunctionNode):
    """Calculate 2D rotation matrix."""

    def __init__(self):
        center_pin = DataInputPin(
            name=PinName("center"),
            dtype=Dtype.any(),
            docs="Center of rotation (x, y)",
        )
        angle_pin = DataInputPin(
            name=PinName("angle"),
            dtype=Dtype(float),
            docs="Rotation angle in degrees",
            default=0.0,
        )
        scale_pin = DataInputPin(
            name=PinName("scale"),
            dtype=Dtype(float),
            docs="Scaling factor",
            default=1.0,
        )
        super().__init__("getRotationMatrix2D", center_pin, angle_pin, scale_pin)

    def apply_function(self, center, angle, scale, **kwargs) -> Any:
        return cv2.getRotationMatrix2D(center, angle, scale)
