# -*- coding: utf-8 -*-

from typing import Any

import cv2

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.opencv._base import OpenCVFunctionNode
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName


class ResizeNode(OpenCVFunctionNode):
    """Resize image to specified dimensions."""

    def __init__(self):
        src_pin = DataInputPin(
            name=PinName("src"),
            dtype=Dtype.any(),
            docs="Source image",
        )
        dsize_pin = DataInputPin(
            name=PinName("dsize"),
            dtype=Dtype.any(),
            docs="Output image size (width, height)",
        )
        fx_pin = DataInputPin(
            name=PinName("fx"),
            dtype=Dtype(float),
            docs="Scale factor along horizontal axis",
            default=0.0,
        )
        fy_pin = DataInputPin(
            name=PinName("fy"),
            dtype=Dtype(float),
            docs="Scale factor along vertical axis",
            default=0.0,
        )
        interpolation_pin = DataInputPin(
            name=PinName("interpolation"),
            dtype=Dtype(int),
            docs="Interpolation method",
            default=cv2.INTER_LINEAR,
        )
        super().__init__(
            "resize", src_pin, dsize_pin, fx_pin, fy_pin, interpolation_pin
        )

    def apply_function(self, src, dsize, fx, fy, interpolation, **kwargs) -> Any:
        return cv2.resize(src, dsize, fx=fx, fy=fy, interpolation=interpolation)
